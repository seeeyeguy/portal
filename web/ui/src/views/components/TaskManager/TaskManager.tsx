import React from "react";
import {
  faArchive,
  faCheckCircle,
  faDownLong,
  faRightFromBracket,
  faTrash,
  faUpLong,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  AutoComplete,
  AutoCompleteCompleteEvent,
} from "primereact/autocomplete";
import { Button } from "primereact/button";
import { Checkbox } from "primereact/checkbox";
import { Column } from "primereact/column";
import { DataTable } from "primereact/datatable";
import { Dropdown } from "primereact/dropdown";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from "primereact/inputtextarea";

import { searchForEmployees } from "services/auth/ldapService";
import { debounce } from "utils/PromiseUtility";

import { ITask } from "views/definitions/ProgramReviewTool.types";

import styles from "views/components/TaskManager/TaskManager.module.css";

const validateTask = (task: ITask) => {
  const missing: string[] = [];
  if (!task.name?.trim()) {
    missing.push("name");
  }
  if (!task.description?.trim()) {
    missing.push("description");
  }
  if (!task.owner?.trim()) {
    missing.push("owner");
  }
  if (!task.targetDate) {
    missing.push("targetDate");
  }
  return missing;
};

/** Properties for the Task Manager component. */
export interface ITaskManagerProps {
  tasks: ITask[];
  isEditing?: boolean;
  externalValidationErrors?: Record<number, string[]>;
  onTasksChange: (updatedTasks: ITask[]) => void;
}

export default function TaskManager({
  tasks,
  isEditing = false,
  externalValidationErrors = {},
  onTasksChange,
}: ITaskManagerProps) {
  const [showArchived, setShowArchived] = React.useState<boolean>(false);

  const [completeCheckedMap, setCompleteCheckedMap] = React.useState<
    Record<number, boolean>
  >({});
  const [localValidationErrors, setLocalValidationErrors] =
    React.useState<Record<number, string[]>>();

  const validationErrors = React.useMemo(
    () => ({
      ...externalValidationErrors,
      ...localValidationErrors,
    }),
    [externalValidationErrors, localValidationErrors]
  );

  /**
   * Called when the user (un)checks the `Completed` box.
   * If checking, required fields (name, description, owner, targetDate)
   * must be present – otherwise they are highlighted.
   */
  const handleCompleteToggle = (index: number, checked: boolean) => {
    const task = tasks[index];

    if (checked) {
      const missing = validateTask(task);

      if (missing.length) {
        // show errors and keep the box unchecked.
        setLocalValidationErrors((prev) => ({ ...prev, [index]: missing }));
        setCompleteCheckedMap((prev) => ({ ...prev, [index]: false }));
        return;
      }

      // all required fields are present so clear any previous errors.
      setLocalValidationErrors((prev) => {
        const copy = { ...prev };
        delete copy[index];
        return copy;
      });

      handleInputChange([
        { index: index, name: "status", value: "Complete" },
        {
          index: index,
          name: "completeDate",
          value: new Date().toISOString().split("T")[0],
        },
      ]);
      setCompleteCheckedMap((prev) => ({ ...prev, [index]: checked }));

      return;
    }

    setCompleteCheckedMap((prev) => ({ ...prev, [index]: checked }));
    // if the user un‑checks, clear the stored completeDate
    handleInputChange([
      {
        index: index,
        name: "completeDate",
        value: null,
      },
    ]);
  };

  const renumberActive = (list: ITask[]) => {
    // Get active tasks and sort them by the current order
    const activeSorted = [...list]
      .filter((t) => !t.archiveDate)
      .sort((a, b) => {
        const oa = a.order ?? Number.MAX_SAFE_INTEGER;
        const ob = b.order ?? Number.MAX_SAFE_INTEGER;
        return oa - ob;
      });

    // Map each active task to its new sequential order.
    const orderMap = new Map<ITask, number>();
    activeSorted.forEach((t, i) => orderMap.set(t, i + 1)); // 1‑based.

    // Build the new list: archived tasks get order null,
    // active tasks get the order from the map.
    return list.map((t) => ({
      ...t,
      order: t.archiveDate ? null : orderMap.get(t)!,
    }));
  };

  const toggleArchive = (index: number) => {
    const newList = [...tasks];
    const task = { ...newList[index] };

    if (task.archiveDate) {
      task.archiveDate = null;
    } else {
      const missing = validateTask(task);

      if (missing.length) {
        // Show errors and keep the box unchecked.
        setLocalValidationErrors((prev) => ({ ...prev, [index]: missing }));
        setCompleteCheckedMap((prev) => ({ ...prev, [index]: false }));
        return;
      }

      // All required fields are present so clear any previous errors.
      setLocalValidationErrors((prev) => {
        const copy = { ...prev };
        delete copy[index];
        return copy;
      });

      task.archiveDate = new Date().toISOString().split("T")[0];
      task.order = null; // Remove from ordering.
      setLocalValidationErrors((prev) => ({ ...prev, [index]: [] }));
    }
    newList[index] = task;

    onTasksChange(renumberActive(newList));
  };

  const lastAddedIndex = React.useRef<number | null>(null);
  const listRef = React.useRef<HTMLUListElement>(null);

  // Whenever the list of tasks changes we scroll to the element.
  React.useEffect(() => {
    if (lastAddedIndex.current === null) return;

    const ul = listRef.current;
    if (!ul) return;

    const li = ul.children[lastAddedIndex.current] as HTMLElement | undefined;
    if (li) {
      li.scrollIntoView({ behavior: "smooth", block: "nearest" });
    } else {
      // Fallback - scroll to bottom.
      ul.scrollTo({ top: ul.scrollHeight, behavior: "smooth" });
    }
    lastAddedIndex.current = null;
  }, [tasks]);

  const addTask = () => {
    const taskPosition = tasks.filter((t) => !t.archiveDate).length + 1;

    const newTask: ITask = {
      id: null,
      paNumber: null,
      reportingPeriod: null,
      order: taskPosition,
      name: "",
      description: "",
      owner: "",
      targetDate: null,
      createDate: new Date().toISOString().split("T")[0],
      completeDate: null,
      archiveDate: null,
      status: "Not Started",
    };

    lastAddedIndex.current = taskPosition;
    onTasksChange([...tasks, newTask]);
  };

  const [filteredSuggestions, setFilteredSuggestions] = React.useState<
    string[]
  >([]);

  const fetchUserOptions = React.useCallback(
    async (searchQuery: AutoCompleteCompleteEvent) => {
      const searchTerm = searchQuery.query;
      if (!searchTerm?.length) return;

      let data = null;

      try {
        let modifiedSearchTerm = searchTerm;
        if (
          modifiedSearchTerm.includes(".") &&
          modifiedSearchTerm[0] !== "." &&
          !modifiedSearchTerm.includes("@")
        ) {
          const splitSearchTerm = modifiedSearchTerm.split(".");
          const [firstName, ...lastName] = splitSearchTerm;
          modifiedSearchTerm = firstName.trim();
          if (
            splitSearchTerm.length > 1 &&
            lastName?.length &&
            lastName[lastName.length - 1].trim()?.length
          ) {
            modifiedSearchTerm = `${modifiedSearchTerm} ${lastName[lastName.length - 1].trim()}`;
          }
        }
        data = await searchForEmployees(modifiedSearchTerm, 1, 25);
      } catch (err) {
        data = {};
      }
      setFilteredSuggestions(
        (data?.data ?? []).map((employee) => employee.email)
      );
    },
    []
  );

  const debouncedFetchUsers = React.useMemo(
    () => debounce(fetchUserOptions, 300),
    [fetchUserOptions]
  );

  const deleteTask = (index: number) => {
    // Task at the given index (real index in tasks).
    const taskToDelete = tasks[index];

    // Create a new array without that task.
    const newList = tasks.filter((_, i) => i !== index);

    // If it was an active task, renumber the remaining active tasks.
    // Archived tasks don’t need order updates.
    if (!taskToDelete.archiveDate) {
      onTasksChange(renumberActive(newList));
    } else {
      onTasksChange(newList);
    }
  };

  /**
   * Move a task up or down **by changing only its `order` field.
   * @param index  – real index of the task in `tasks`
   * @param up     – true  → move up (decrease order)
   *                 false → move down (increase order)
   */
  const moveTask = (index: number, up: boolean) => {
    const task = tasks[index];
    if (task.archiveDate) return; // ignore archived items.
    if (task.order == null) return; // nothing to move.

    const newOrder = task.order + (up ? -1 : 1);

    // Find the neighbor task that currently has the target order.
    const neighborIdx = tasks.findIndex(
      (t) => !t.archiveDate && t.order === newOrder
    );
    if (neighborIdx === -1) return; // already at the top or bottom.

    // Swap the order values.
    const newList = [...tasks];
    newList[index] = { ...newList[index], order: newOrder };
    newList[neighborIdx] = { ...newList[neighborIdx], order: task.order };
    onTasksChange(newList);
  };

  /* eslint-disable @typescript-eslint/no-explicit-any */
  const handleInputChange = (
    changes: { index: number; name: string; value: any }[]
  ) => {
    const newTaskList = [...tasks];

    changes.forEach(({ index, name, value }) => {
      newTaskList[index] = {
        ...newTaskList[index],
        [name]: value,
      };
    });

    onTasksChange(newTaskList);
  };

  const activeTasks = React.useMemo(() => {
    return tasks
      .filter((t) => !t.archiveDate)
      .sort((a, b) => (a.order ?? 0) - (b.order ?? 0));
  }, [tasks]);

  const archivedTasks = React.useMemo(() => {
    return tasks
      .filter((t) => t.archiveDate)
      .sort((a, b) => (a.archiveDate! < b.archiveDate! ? 1 : -1)); // Newest first.
  }, [tasks]);

  const displayed = React.useMemo(() => {
    return showArchived ? [...activeTasks, ...archivedTasks] : activeTasks;
  }, [showArchived, activeTasks, archivedTasks]);

  // Expansion content to show the description of the task.
  const [expandedRows, setExpandedRows] = React.useState<ITask[]>([]);
  const rowExpansionTemplate = (task: ITask) => (
    <div
      className={styles["task-description"]}
      style={{ whiteSpace: "pre-wrap" }}
    >
      {task.description?.trim() ? (
        task.description
      ) : (
        <i style={{ color: "#666" }}>No description</i>
      )}
    </div>
  );
  if (!isEditing) {
    const handleRowToggle = (e: { data: ITask[] }) => {
      // Show only the last row the user opened.
      const latest = e.data.slice(-1);
      setExpandedRows(latest);
    };

    return (
      <div
        className={styles["task-manager"]}
        style={{ height: "400px", overflowY: "auto" }}
      >
        {/* PrimeReact table – active tasks only */}
        <DataTable
          expandedRows={expandedRows}
          onRowToggle={handleRowToggle}
          rowExpansionTemplate={rowExpansionTemplate}
          value={activeTasks}
          tableStyle={{ minWidth: "100%" }}
          emptyMessage="No tasks to display"
          scrollable
          scrollHeight="flex"
        >
          {/* Expander column – click to open description */}
          <Column expander bodyClassName={styles["compact-cell"]} />

          {/* Task name */}
          <Column
            field="name"
            header="Name"
            bodyClassName={styles["compact-cell"]}
            body={(row) => {
              const txt = row.name ?? "";
              const display = txt.length > 80 ? `${txt.slice(0, 80)}…` : txt;
              return (
                <strong title={txt.length === display.length ? "" : txt}>
                  {display}
                </strong>
              );
            }}
          />

          {/* Owner */}
          <Column
            field="owner"
            header="Owner"
            bodyClassName={`${styles["compact-cell"]} ${styles["owner-cell"]}`}
            body={(row) => (
              <span className={styles["owner-cell"]}>
                {
                  // Convert to Firstname Lastname.
                  row.owner
                    .split("@")[0]
                    .split(".")
                    .map(
                      (part: string) =>
                        part.charAt(0).toUpperCase() + part.slice(1)
                    )
                    .join(" ")
                }
              </span>
            )}
          />

          {/* Target date */}
          <Column
            field="targetDate"
            header="Target"
            bodyClassName={styles["compact-cell"]}
            style={{ width: "120px", textAlign: "center" }}
            body={(row) =>
              row.targetDate ? (
                <span className={styles["task-date"]}>{row.targetDate}</span>
              ) : (
                <i>–</i>
              )
            }
          />

          {/* Complete date */}
          <Column
            field="completeDate"
            header="Completed"
            bodyClassName={styles["compact-cell"]}
            style={{ width: "120px", textAlign: "center" }}
            body={(row) =>
              row.completeDate ? (
                <span className={styles["task-date"]}>{row.completeDate}</span>
              ) : (
                <i>–</i>
              )
            }
          />

          {/* Status */}
          <Column
            field="status"
            header="Status"
            bodyClassName={styles["compact-cell"]}
            style={{ width: "100px" }}
            body={(row) => (
              <span className={styles["task-status"]}>{row.status}</span>
            )}
          />

          {/* Completed icon column */}
          <Column
            header=" "
            bodyClassName={styles["compact-cell"]}
            style={{ width: "20px" }}
            body={(row) =>
              row.completeDate ? (
                <FontAwesomeIcon
                  icon={faCheckCircle}
                  color="green"
                  className={styles["task-complete-icon"]}
                />
              ) : null
            }
          />
        </DataTable>
      </div>
    );
  }

  return (
    <div className={styles["task-manager"]}>
      <header>
        <Button
          type="button"
          onClick={addTask}
          className={styles["add-task-button"]}
        >
          Add Task
        </Button>
        <label className={styles["show-archived-label"]}>
          <Checkbox
            checked={showArchived}
            onChange={(e) => setShowArchived(e.checked ?? false)}
          />
          Show Archived
        </label>
      </header>

      <ul ref={listRef}>
        {displayed.map((task, displayIdx) => {
          // Find the *real* index in the full `taskList` – needed for
          // edit / delete / archive actions that mutate the underlying array.
          const realIdx = tasks.findIndex((t) => t === task);

          // Helper to add the error style to an input.
          const hasError = (field: string) =>
            validationErrors[realIdx]?.includes(field);

          const completedChecked =
            completeCheckedMap[realIdx] ?? !!task.completeDate;

          return (
            <li
              key={`${displayIdx}-${task.id}`}
              className={styles["task-card"]}
            >
              <div className={styles["task-col"]}>
                <div className={styles["task-row"]}>
                  {/* ----- editable fields ----- */}
                  <InputText
                    type="text"
                    tooltip="Task Name"
                    value={task.name}
                    disabled={!!task.archiveDate || !!task.completeDate}
                    onChange={(e) =>
                      handleInputChange([
                        { index: realIdx, name: "name", value: e.target.value },
                      ])
                    }
                    placeholder="Task Name"
                    className={`${styles["task-input"]}`}
                    invalid={hasError("name")}
                    maxLength={1028}
                  />
                  <AutoComplete
                    tooltip="Owner"
                    value={task.owner ?? ""}
                    suggestions={filteredSuggestions}
                    disabled={!!task.archiveDate || !!task.completeDate}
                    completeMethod={debouncedFetchUsers}
                    onDropdownClick={fetchUserOptions}
                    onChange={(e) =>
                      handleInputChange([
                        {
                          index: realIdx,
                          name: "owner",
                          value: e.target.value,
                        },
                      ])
                    }
                    placeholder="Owner"
                    className={`${styles["task-input"]} ${styles["autocomplete-input"]}`}
                    invalid={hasError("owner")}
                    maxLength={128}
                    dropdown
                    showEmptyMessage={true}
                  />
                  <InputText
                    type="date"
                    tooltip="Target Date"
                    value={task.targetDate ?? ""}
                    disabled={!!task.archiveDate || !!task.completeDate}
                    onChange={(e) =>
                      handleInputChange([
                        {
                          index: realIdx,
                          name: "targetDate",
                          value: e.target.value,
                        },
                      ])
                    }
                    placeholder="Target Date"
                    className={`${styles["task-input"]} ${styles["date-input"]}`}
                    invalid={hasError("targetDate")}
                  />

                  <InputText
                    type={
                      !!task.archiveDate || !completedChecked ? "text" : "date"
                    }
                    tooltip="Complete Date"
                    value={task.completeDate ?? ""}
                    disabled={!!task.archiveDate || !completedChecked}
                    onChange={(e) =>
                      handleInputChange([
                        {
                          index: realIdx,
                          name: "completeDate",
                          value: e.target.value,
                        },
                      ])
                    }
                    placeholder="Complete Date"
                    className={`${styles["task-input"]} ${styles["date-input"]}`}
                  />

                  <Dropdown
                    value={task.status}
                    tooltip="Current Status"
                    disabled={!!task.archiveDate || !!task.completeDate}
                    onChange={(e) =>
                      handleInputChange([
                        {
                          index: realIdx,
                          name: "status",
                          value: e.target.value,
                        },
                      ])
                    }
                    placeholder="Status"
                    className={`${styles["task-input"]} ${styles["dropdown-input"]}`}
                    options={["Not Started", "In Progress", "Complete"]}
                  />
                </div>
                <div className={styles["task-row"]}>
                  <InputTextarea
                    value={task.description ?? undefined}
                    tooltip="Description"
                    disabled={!!task.archiveDate || !!task.completeDate}
                    onChange={(e) =>
                      handleInputChange([
                        {
                          index: realIdx,
                          name: "description",
                          value: e.target.value,
                        },
                      ])
                    }
                    placeholder="Description"
                    className={`${styles["task-input"]} ${styles["area-input"]}`}
                    invalid={hasError("description")}
                    maxLength={4096}
                  />

                  <span className={styles["action-list"]}>
                    {/* ----- action buttons ----- */}

                    <div className={styles["checkbox-wrapper"]}>
                      <Checkbox
                        checked={completedChecked}
                        tooltip="Complete Task"
                        onChange={(e) =>
                          handleCompleteToggle(realIdx, e.checked ?? false)
                        }
                        disabled={!!task.archiveDate}
                      />
                    </div>

                    {/* Up / Down only for **active** tasks */}
                    {!task.archiveDate && (
                      <>
                        <Button
                          onClick={() => moveTask(realIdx, true)} // up
                          tooltip="Move Up"
                          disabled={displayIdx === 0}
                          className={`${styles["task-arrow"]} ${styles["task-action-button"]}`}
                          type="button"
                        >
                          <FontAwesomeIcon
                            className={styles["task-action-icon"]}
                            icon={faUpLong}
                          />
                        </Button>
                        <Button
                          onClick={() => moveTask(realIdx, false)} // down
                          tooltip="Move Down"
                          className={`${styles["task-arrow"]} ${styles["task-action-button"]}`}
                          disabled={displayIdx === activeTasks.length - 1}
                          type="button"
                        >
                          <FontAwesomeIcon
                            className={styles["task-action-icon"]}
                            icon={faDownLong}
                          />
                        </Button>
                      </>
                    )}

                    {/* Archive / Un‑archive button */}
                    <Button
                      onClick={() => toggleArchive(realIdx)}
                      tooltip={`${task.archiveDate ? "Unarchive Task" : "Archive Task"}`}
                      className={`${styles["task-archive"]} ${styles["task-action-button"]}`}
                      type="button"
                    >
                      <FontAwesomeIcon
                        className={styles["task-action-icon"]}
                        icon={task.archiveDate ? faRightFromBracket : faArchive}
                        rotation={task.archiveDate ? 270 : undefined}
                      />
                    </Button>

                    <Button
                      onClick={() => deleteTask(realIdx)}
                      tooltip="Delete Task"
                      className={`${styles["task-delete"]} ${styles["task-action-button"]}`}
                      type="button"
                    >
                      <FontAwesomeIcon
                        className={styles["task-action-icon"]}
                        icon={faTrash}
                      />
                    </Button>
                  </span>
                </div>
              </div>
              <span></span>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
