interface IWebSocketService<T, U> {
  connect(url: string): void;
  sendMessage(message: T): void;
  onMessage(callback: (message: U) => void): void;
  removeListener(callback: (message: U) => void): void;
  disconnect(): void;
}

const NORMAL_CLOSURE: number = 1000;

class WebSocketService<T, U> implements IWebSocketService<T, U> {
  private socket: WebSocket | null = null;
  private callbacks: Map<(message: U) => void, (message: U) => void> =
    new Map();

  private url: string | null = null;
  private RECONNECT_ATTEMPTS: number = 0;
  private MAX_RECONNECT_ATTEMPTS: number = 5;
  private RECONNECT_DELAY: number = 3000;

  connect(url: string): void {
    this.url = url;
    this.attemptConnect();
  }

  private attemptConnect(): void {
    if (this.MAX_RECONNECT_ATTEMPTS <= this.RECONNECT_ATTEMPTS) {
      console.error("Max reconnect attempts reached.");
      return;
    }

    if (!this.url) {
      console.error("Url has not been set.");
      return;
    }

    this.socket = new WebSocket(this.url);
    this.RECONNECT_ATTEMPTS++;

    this.socket.onopen = () => {
      console.log(`WebSocket connected to ${this.url}.`);
      this.RECONNECT_ATTEMPTS = 0;
    };

    this.socket.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event?.data ?? "{}");
        this.callbacks.forEach((cb) => cb(data));
      } catch (error) {
        console.error(`Error parsing WebSocket message: ${error}`);
      }
    };

    this.socket.onclose = (event) => {
      console.log(
        `WebSocket disconnected from ${this.url}. Code: ${event.code}, Reason: ${event.reason}.`
      );
      if (event.code !== NORMAL_CLOSURE) {
        setTimeout(() => this.attemptConnect(), this.RECONNECT_DELAY);
      }
    };

    this.socket.onerror = (error: Event) => {
      console.error(`WebSocket error: ${error}`);
    };
  }

  sendMessage(arg: T): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(JSON.stringify(arg));
    } else {
      console.warn("WebSocket is not connected.");
    }
  }

  onMessage(callback: (arg: U) => void): void {
    this.callbacks.set(callback, callback);
  }

  removeListener(callback: (arg: U) => void): void {
    this.callbacks.delete(callback);
  }

  disconnect(): void {
    console.log(`WebSocket disconnecting from ${this.url}`);
    if (this.socket) {
      this.socket.close(NORMAL_CLOSURE, "Normal closure");
      this.socket = null;
      this.RECONNECT_ATTEMPTS = 0;
    }
  }
}

export { WebSocketService };
