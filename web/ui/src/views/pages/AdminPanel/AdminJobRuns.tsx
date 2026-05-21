import React from "react"
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";
import { useJobRuns } from "hooks/useJobRuns";
import { IJobRun, JobStatus, IRegistryJob } from "views/pages/AdminPanel/JobRun.types"
import { toast  }from "react-toastify";

import { Dropdown, DropdownChangeEvent } from "primereact/dropdown"
import { DataTable } from "primereact/datatable"
import { Column } from "primereact/column"


const path = "/admin/job-runs";


import styles from "views/containers/AdminControls/AdminControls.module.css"


export default function AdminJobRuns() {

    const {jobRuns, registry, loading, error, runJob, refresh: fetchJobRuns } = useJobRuns()
    // const [selectedJob, setSelectedJob] = React.useState<IRegistryJob | null>(null);

    const handlePlay = async (registryJob: IRegistryJob) => {
        try {
            console.log(`Job name: ${registryJob.jobName}`);
            await runJob(registryJob.jobName);
            toast.success(`Job "${registryJob.jobName}" started`);
        } catch {
            toast.error(`Failed to start job $${registryJob.jobName}`)
        }
    }

    const jobFuctionTemplate = (row: IJobRun) => (
            <div style={{ display: "flex", gap: "0.5rem"}}>
                <button
                    onClick={() => handlePlay(row.jobName)}
                    aria-label="update form card button"
                >
                    Run Job
                </button>
            </div>
    )

    return (
        <AdminPanel path={path}>
            <MaintenanceBanner page={path} />
            <main>
                <header>
                    <h1>Server Jobs</h1>
                </header>
                <div style={{ display: "flex", flexDirection: "row", gap: "2rem"}}>
                    <div>
                        <DataTable value={jobRuns} header="Job History" className={styles["data-table"]}>
                            <Column field="jobName" header="Job Name"></Column>
                            <Column field="startedAt" header="Start time"></Column>
                            <Column field="finishedAt" header="Finish time"></Column>
                            <Column field="status" header="Status"></Column>
                            <Column field="user" header="User"></Column>
                        </DataTable>
                    </div>
                    <div>
                        <DataTable value={registry} header="Job Control" className={styles["data-table"]} tableStyle={{ minWidth: "100%"}} >
                            <Column field="jobName" header="Job Name"></Column>
                            <Column header="Control" body={jobFuctionTemplate}></Column>
                        </DataTable>
                    </div>
                </div>
            </main>
        </AdminPanel>
    );
}

