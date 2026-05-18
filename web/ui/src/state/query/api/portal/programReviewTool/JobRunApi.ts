import { DELETE, POST, PUT } from "definitions/RequestConstants";
import endpoints from "services/api";
import api from "state/query/api";

// TODO: might need a content helper but who knows.

type TApiJobRunRequest = {
    job_name: string
}

// fetching will be an array of these
type TJobRun = {
    id: number;
    created: string;
    job_name: string;
    user: string;
    status: string;
    running: string;
    started_at: string | undefined;
    finished_at: string | undefined;
};

const jobRunApi = api.injectEndpoints({
    endpoints: (builder) => ({
        createJobRun: builder.query<TApiJobRunRequest, string>({
            query: (body: TApiJobRunRequest) => ){
                url: endpoints.PORTAL.JO
            }
        })
        getJobs
        /* getJobRuns TODO: will implement later for history */
    })
})




