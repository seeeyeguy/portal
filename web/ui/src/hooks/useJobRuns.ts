import { useState, useEffect, useCallback } from "react";
import { snakeCaseToCamelCase } from "utils/CaseTransformUtility";
import { getCookie } from "utils/CookieUtility";
import { IJobRun, IJobRegistryJob } from "views/definitions/ProgramReviewTool.types";

const BASE_URL = "/api/v1/program-review-tool"

export function useJobRuns() {
    const [jobRuns, setJobRuns] = useState<any[]>([])
    const [registry, setRegistry] = useState<any[]>([])
    const [loading, setLoading] = useState<boolean>(false)
    const [error, setError] = useState<string | null>(null)

    const fetchJobRuns = useCallback(async () => {
        try {
            setLoading(true);
            const res = await fetch(`${BASE_URL}/job-run`);
            const data = await res.json();
            setJobRuns(snakeCaseToCamelCase(data) as IJobRun[]);
        } catch(err) {
            setError(err instanceof Error ? err.message : String(err))
        } finally {
            setLoading(false);
        }
    }, []);

    const fetchRegistry = useCallback(async () => {
        try {
            const res = await fetch(`${BASE_URL}/job-run/registry`);
            const data = await res.json();
            setRegistry(snakeCaseToCamelCase(data) as IJobRegistryJob[]);
        } catch(err) {
            setError(err instanceof Error ? err.message : String(err))
        }
    }, [])

    const runJob = useCallback(
        async (jobName: string) => {
            const res = await fetch(`${BASE_URL}/job-run`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ job_name: jobName })
            });
            if (!res.ok) throw new Error("Failed to start job");
            await fetchJobRuns();
        }, [fetchJobRuns]);

    useEffect( () => {
        fetchJobRuns();
        fetchRegistry();
    }, [fetchJobRuns, fetchRegistry])

    return {jobRuns, registry, loading, error, runJob, refresh: fetchJobRuns };
}
