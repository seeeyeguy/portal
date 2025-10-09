import endpoints from "services/api";
import { WebSocketService } from "services/api/webSocketsHelper";
import api from "state/query/api";

export type IPendingRequest = {
  requestId: number;
  subfunctions: number[];
  originator: string;
  stage: number;
};

export interface IApiRequestNotification {
  content: IPendingRequest[];
  status: number | null;
}

const webSocketService = new WebSocketService<
  object,
  IApiRequestNotification
>();

const requestNotificationWebSocketsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    subscribeToRequestNotification: builder.query<
      IApiRequestNotification,
      void
    >({
      queryFn: () => ({
        data: {
          content: [],
          status: null,
        },
      }),
      async onCacheEntryAdded(
        _,
        { updateCachedData, cacheDataLoaded, cacheEntryRemoved }
      ) {
        try {
          const url = endpoints.PORTAL.REQUEST.REQUEST_NOTIFICATION.WS;

          await cacheDataLoaded;

          // Check if socket is available before connecting.
          if (
            !webSocketService["socket"] ||
            webSocketService["socket"].readyState !== WebSocket.OPEN
          ) {
            webSocketService.connect(url);
          }

          // Callback function that updates the cached data
          // once the message is received on the socket.
          const handleMessage = async (message: IApiRequestNotification) => {
            updateCachedData((draft) => {
              draft.content = message?.content;
              draft.status = message?.status;
            });
          };

          webSocketService.onMessage(handleMessage);

          // Will resolve when the cache subscription is no longer active
          // so the following actions can executed (i.e disconnecting the
          // socket.)
          await cacheEntryRemoved;

          webSocketService.removeListener(handleMessage);
          if (!webSocketService["callbacks"].size) {
            webSocketService.disconnect();
          }
        } catch (error) {
          console.error(`Websocket subscription error: ${error}`);
        }
      },
    }),
    refreshRequestNotifications: builder.mutation<null, void>({
      queryFn: () => {
        webSocketService.sendMessage({});
        return { data: null };
      },
    }),
  }),
});

export default requestNotificationWebSocketsApi;
export const {
  useSubscribeToRequestNotificationQuery,
  useRefreshRequestNotificationsMutation,
} = requestNotificationWebSocketsApi;
