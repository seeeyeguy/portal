import React from "react";
import { Meta, StoryObj } from "@storybook/react";

import TaskManager, { ITask } from "views/components/TaskManager/TaskManager";

const meta: Meta<typeof TaskManager> = {
  title: "TaskManager",
  component: TaskManager,
  tags: ["autodocs"],
  parameters: {
    // More on how to position stories at: https://storybook.js.org/docs/configure/story-layout.
    layout: "padded",
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    isEditing: true,
    tasks: [],
  },
  render: (args) => {
    const [tasks, setTasks] = React.useState<ITask[]>(args.tasks);

    return (
      <TaskManager
        {...args}
        tasks={tasks}
        onTasksChange={(e) => {
          console.log(e);
          setTasks(e);
        }}
      />
    );
  },
};

export const WithTasks: Story = {
  args: {
    tasks: [
      {
        id: 1,
        order: 1,
        name: "Task 1",
        description: "Description for task 1",
        owner: "John Doe",
        targetDate: "2023-10-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "",
        archiveDate: null,
        status: "In progress",
      },
      {
        id: 2,
        order: 2,
        name: "Task 2",
        description: "Description for task 2",
        owner: "Jane Smith",
        targetDate: "2023-11-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "2025-09-12",
        archiveDate: null,
        status: "Complete",
      },
      {
        id: 3,
        order: null,
        name: "Task 3 Archived",
        description: "Description for task 3",
        owner: "Jane Smith",
        targetDate: "2023-11-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "",
        archiveDate: "2025-09-12T12:39:16.207Z",
        status: "Abandoned",
      },
      {
        id: 4,
        order: null,
        name: "Task 4 Archived",
        description: "Description for task 4",
        owner: "Jane Smith",
        targetDate: "2023-11-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "2023-11-01",
        archiveDate: "2025-09-12T12:39:16.207Z",
        status: "Completed",
      },
    ],
  },
  render: (args) => {
    const [tasks, setTasks] = React.useState<ITask[]>(args.tasks);

    return (
      <TaskManager
        {...args}
        tasks={tasks}
        onTasksChange={(e) => {
          console.log(e);
          setTasks(e);
        }}
      />
    );
  },
};

export const EditingTasks: Story = {
  args: {
    isEditing: true,
    tasks: [
      {
        id: 1,
        order: 1,
        name: "Task 1",
        description: "Description for task 1",
        owner: "John Doe",
        targetDate: "2023-10-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "",
        archiveDate: null,
        status: "In progress",
      },
      {
        id: 2,
        order: 2,
        name: "Task 2",
        description: "Description for task 2",
        owner: "Jane Smith",
        targetDate: "2023-11-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "2025-09-12",
        archiveDate: null,
        status: "Complete",
      },
      {
        id: 3,
        order: null,
        name: "Task 3 Archived",
        description: "Description for task 3",
        owner: "Jane Smith",
        targetDate: "2023-11-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "",
        archiveDate: "2025-09-12T12:39:16.207Z",
        status: "Abandoned",
      },
      {
        id: 4,
        order: null,
        name: "Task 4 Archived",
        description: "Description for task 4",
        owner: "Jane Smith",
        targetDate: "2023-11-01",
        createDate: "2025-09-12T12:39:16.207Z",
        completeDate: "2023-11-01",
        archiveDate: "2025-09-12T12:39:16.207Z",
        status: "Completed",
      },
    ],
  },
  render: (args) => {
    const [tasks, setTasks] = React.useState<ITask[]>(args.tasks);

    return (
      <TaskManager
        {...args}
        tasks={tasks}
        onTasksChange={(e) => {
          console.log(e);
          setTasks(e);
        }}
      />
    );
  },
};
