import React from "react"
import MaintenanceBanner from "views/containers/MaintenanceBanner/MaintenanceBanner";
import AdminPanel from "views/pages/AdminPanel/AdminPanel";
import { Dropdown, DropdownChangeEvent } from "primereact/dropdown"

import { IJobRun, JobStatus, IRegistryJob } from "views/pages/AdminPanel/JobRun.types"
import { useJobRuns } from "hooks/useJobRuns";

const path = "/admin/job-runs";


import styles from "views/containers/AdminControls/AdminControls.module.css"


export default function AdminJobRuns() {

    const {jobRuns, registry, loading, error, runJob, refresh: fetchJobRuns } = useJobRuns()
    const [selectedJob, setSelectedJob] = React.useState<IRegistryJob | null>(null);

    return (
        <AdminPanel path={path}>
            <MaintenanceBanner page={path} />
            <main>
                <header>
                    <h1>Server Jobs</h1>
                </header>
            </main>
            <div
                className={styles["admin-controls"]}
                aria-description="job run admin controls"
            >
                <Dropdown
                    value={selectedJob}
                    options={registry}
                    optionLabel="name"
                    placeholder="Select a job"
                    onChange={(e: DropdownChangeEvent) => setSelectedJob(e.value)}
                    className={styles["admin-dropdown-filter"]}
                />
            </div>
        </AdminPanel>
    );
}

