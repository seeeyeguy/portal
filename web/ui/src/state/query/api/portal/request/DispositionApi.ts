import { IDisposition } from "definitions/portal/request/Disposition.types";
import endpoints from "services/api";
import { WebSocketService } from "services/api/webSocketsHelper";
import api from "state/query/api";
import {
  IApiDisposition,
  transformDispositionRecord,
} from "state/query/api/portal/request/DispositionHelper";
import requestApi from "state/query/api/portal/request/RequestApi";
import store from "state/store/store";

export type TApiWSPostDispositionRequest = {
  disposition: "APPROVED" | "REJECTED" | "REVISE";
  justification: string;
};

const webSocketService = new WebSocketService<
  TApiWSPostDispositionRequest & { request_id: number },
  IApiDisposition
>();

const dispositionWebSocketsApi = api.injectEndpoints({
  endpoints: (builder) => ({
    subscribeToDisposition: builder.query<IDisposition[], void>({
      queryFn: () => ({ data: [] }),
      async onCacheEntryAdded(
        getRequestArgs,
        { updateCachedData, cacheDataLoaded, cacheEntryRemoved }
      ) {
        try {
          const url = endpoints.PORTAL.REQUEST.DISPOSITION.WS;

          await cacheDataLoaded;

          if (
            !webSocketService["socket"] ||
            webSocketService["socket"].readyState !== WebSocket.OPEN
          ) {
            webSocketService.connect(url);
          }

          const handleMessage = async (message: IApiDisposition) => {
            updateCachedData((draft) => {
              draft.push(transformDispositionRecord(message));
            });
            const { refetch } = store.dispatch(
              requestApi.endpoints.getRequests.initiate(
                (getRequestArgs as object | null | undefined) ?? {}
              )
            );
            refetch();
          };

          webSocketService.onMessage(handleMessage);

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
    sendDisposition: builder.mutation<null, TApiWSPostDispositionRequest>({
      queryFn: (body: TApiWSPostDispositionRequest & { requestId: number }) => {
        webSocketService.sendMessage({
          request_id: body.requestId,
          disposition: body.disposition,
          justification: body.justification,
        });
        return { data: null };
      },
      invalidatesTags: ["Request"],
    }),
  }),
});

export default dispositionWebSocketsApi;
export const { useSendDispositionMutation, useSubscribeToDispositionQuery } =
  dispositionWebSocketsApi;
