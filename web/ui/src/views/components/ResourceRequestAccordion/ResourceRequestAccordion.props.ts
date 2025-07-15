import { IRequest } from "definitions/portal/request/Request.types.ts";
import {
  ITransition,
  ITransitionGraph,
} from "definitions/portal/request/Transition.types.ts";

export const ExampleRequest: IRequest = {
  id: 260,
  resource: {
    id: 260,
    employeeLevels: [
      {
        id: 1,
        name: "Employee",
        description: "Employee Level 1.",
        created: new Date("2025-04-01T12:20:23.500906-04:00"),
        modified: new Date("2025-04-01T12:20:23.500912-04:00"),
        level: 1,
      },
      {
        id: 2,
        name: "Manager",
        description: "Manager Level 1.",
        created: new Date("2025-04-01T12:20:23.500915-04:00"),
        modified: new Date("2025-04-01T12:20:23.500917-04:00"),
        level: 2,
      },
      {
        id: 3,
        name: "Executive",
        description: "Executive Level 1.",
        created: new Date("2025-04-01T12:20:23.500921-04:00"),
        modified: new Date("2025-04-01T12:20:23.500923-04:00"),
        level: 3,
      },
    ],
    subfunctions: [
      {
        id: 33,
        function: {
          id: 8,
          name: "Supply Chain",
          description: "TBA",
          created: new Date("2025-04-01T12:21:05.069588-04:00"),
          modified: new Date("2025-04-01T12:21:05.069594-04:00"),
        },
        name: "Warehouse",
        description: "TBA",
        created: new Date("2025-04-01T12:21:05.080511-04:00"),
        modified: new Date("2025-04-01T12:21:05.080517-04:00"),
      },
    ],
    tags: [
      {
        id: 113,
        created: new Date("2025-04-01T12:21:05.121490-04:00"),
        modified: new Date("2025-04-01T12:21:05.121492-04:00"),
        label: "capacity",
      },
    ],
    description:
      "Evaluates forecasted picks and moves, comparing to existing capacity.",
    created: new Date("2025-04-01T12:21:39.346546-04:00"),
    uid: "7b36fe04-c5e4-4c07-b1b2-60ff277c8558",
    revisionNumber: 1,
    name: "Warehouse Resource Capacity Forecast",
    url: "https://tableau.l3harris.com/#/workbooks/10656/views",
    thumbnail: null,
    type: "tableau",
    download: false,
    active: true,
    deleted: false,
    previousRevision: null,
    primaryPointOfContact: "ben.parker@harris.com",
    favoritedBy: [],
    site: [],
  },
  originator: {
    id: 48,
    user: {
      id: 48,
      username: "ben.parker@harris.com",
      email: "ben.parker@harris.com",
      firstName: "Ben",
      lastName: "Parker",
      isActive: true,
    },
    role: {
      id: 3,
      created: new Date("2025-04-01T12:20:23.500627-04:00"),
      name: "Data Steward",
      description: "Data Steward.",
      level: 3,
    },
    stage: [],
    subfunctions: [
      {
        id: 24,
        function: {
          id: 8,
          name: "Supply Chain",
          description: "TBA",
          created: new Date("2025-04-01T12:21:05.069588-04:00"),
          modified: new Date("2025-04-01T12:21:05.069594-04:00"),
        },
        name: "Compliance - MMAS",
        description: "TBA",
        created: new Date("2025-04-01T12:21:05.079704-04:00"),
        modified: new Date("2025-04-01T12:21:05.079709-04:00"),
      },
    ],
    accessGrantedDate: new Date("2025-04-01T12:21:05.064115-04:00"),
    accessRevokedDate: null,
  },
  created: new Date("2025-04-01T12:21:39.376229-04:00"),
  modified: new Date("2025-04-01T12:21:39.376235-04:00"),
  status: "APPROVED",
  transitions: {
    latest: 1,
    nodes: {
      "1": {
        id: 1,
        request: 260,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-01T12:21:39.411497-04:00"),
        dispositions: [],
      },
    },
  },
};

export const ExampleTransitions: { [key: string]: ITransitionGraph } = {
  Default: {
    latest: 2,
    nodes: {
      1: {
        id: 1,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      2: {
        id: 2,
        request: 1,
        stage: {
          id: 2,
          name: "Submitted",
          description: "A resource was submitted",
          level: 2,
        },
        previousTransition: 1,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
    },
  },
  Revise: {
    latest: 3,
    nodes: {
      1: {
        id: 1,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      2: {
        id: 2,
        request: 1,
        stage: {
          id: 2,
          name: "Submitted",
          description: "A resource was submitted",
          level: 2,
        },
        previousTransition: 1,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      3: {
        id: 3,
        request: 1,
        stage: {
          id: 4,
          name: "Revise",
          description: "An edit to the draft was requested.",
          level: 4,
        },
        previousTransition: 2,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
    },
  },
  BusinessProcessExpertApproved: {
    latest: 3,
    nodes: {
      1: {
        id: 1,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      2: {
        id: 2,
        request: 1,
        stage: {
          id: 2,
          name: "Submitted",
          description: "A resource was submitted",
          level: 2,
        },
        previousTransition: 1,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      3: {
        id: 3,
        request: 1,
        stage: {
          id: 3,
          name: "Approved by Business Process Expert",
          description:
            "A resource was approved by the Business Process Expert.",
          level: 3,
        },
        previousTransition: 2,
        created: new Date("2025-04-24T11:59:31.805896-04:00"),
      },
    },
  },
  BusinessProcessExpertRejected: {
    latest: 5,
    nodes: {
      1: {
        id: 1,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      2: {
        id: 2,
        request: 1,
        stage: {
          id: 2,
          name: "Submitted",
          description: "A resource was submitted",
          level: 2,
        },
        previousTransition: 1,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      3: {
        id: 3,
        request: 1,
        stage: {
          id: 4,
          name: "Revise",
          description: "An edit to the draft was requested.",
          level: 4,
        },
        previousTransition: 2,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      5: {
        id: 5,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: 3,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      6: {
        id: 6,
        request: 1,
        stage: {
          id: 2,
          name: "Submitted",
          description: "A resource was submitted",
          level: 2,
        },
        previousTransition: 5,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      7: {
        id: 7,
        request: 1,
        stage: {
          id: 5,
          name: "Rejected by Business Process Expert",
          description:
            "A resource was rejected by the Business Process Expert.",
          level: 100,
        },
        previousTransition: 6,
        created: new Date("2025-04-24T11:59:31.805896-04:00"),
      },
    },
  },
  SuperUserApproved: {
    latest: 4,
    nodes: {
      1: {
        id: 1,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      2: {
        id: 2,
        request: 1,
        stage: {
          id: 2,
          name: "Submitted",
          description: "A resource was submitted",
          level: 2,
        },
        previousTransition: 1,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
      3: {
        id: 3,
        request: 1,
        stage: {
          id: 3,
          name: "Approved by Business Process Expert",
          description:
            "A resource was approved by the Business Process Expert.",
          level: 3,
        },
        previousTransition: 2,
        created: new Date("2025-04-24T11:59:31.805896-04:00"),
      },
      4: {
        id: 4,
        request: 1,
        stage: {
          id: 6,
          name: "Approved by a Superuser",
          description: "A resource was approved by a Superuser.",
          level: 99,
        },
        previousTransition: 3,
        created: new Date("2025-04-24T11:59:31.805896-04:00"),
      },
    },
  },
  ActiveExample: {
    latest: 1,
    nodes: {
      1: {
        id: 1,
        request: 1,
        stage: {
          id: 1,
          name: "Draft",
          description: "A resource was created.",
          level: 1,
        },
        previousTransition: null,
        created: new Date("2025-04-24T11:59:30.805896-04:00"),
      },
    },
  },
};

export const ActiveTransitions: ITransition[] = [
  {
    id: 1,
    request: 1,
    stage: {
      id: 1,
      name: "Draft",
      description: "A resource was created.",
      level: 1,
    },
    previousTransition: null,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 2,
    request: 1,
    stage: {
      id: 2,
      name: "Submitted",
      description: "A resource was submitted",
      level: 2,
    },
    previousTransition: 1,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 3,
    request: 1,
    stage: {
      id: 3,
      name: "Approved by Business Process Expert",
      description: "A resource was approved by the Business Process Expert.",
      level: 3,
    },
    previousTransition: 2,
    created: new Date("2025-04-24T11:59:31.805896-04:00"),
  },
  {
    id: 4,
    request: 1,
    stage: {
      id: 4,
      name: "Revise",
      description: "An edit to the draft was requested.",
      level: 4,
    },
    previousTransition: 3,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 5,
    request: 1,
    stage: {
      id: 1,
      name: "Draft",
      description: "A resource was created.",
      level: 1,
    },
    previousTransition: 4,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 6,
    request: 1,
    stage: {
      id: 2,
      name: "Submitted",
      description: "A resource was submitted",
      level: 2,
    },
    previousTransition: 5,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 7,
    request: 1,
    stage: {
      id: 3,
      name: "Approved by Business Process Expert",
      description: "A resource was approved by the Business Process Expert.",
      level: 3,
    },
    previousTransition: 6,
    created: new Date("2025-04-24T11:59:31.805896-04:00"),
  },
  {
    id: 8,
    request: 1,
    stage: {
      id: 6,
      name: "Approved by a Superuser",
      description: "A resource was approved by a Superuser.",
      level: 99,
    },
    previousTransition: 7,
    created: new Date("2025-04-24T11:59:31.805896-04:00"),
  },
  {
    id: 9,
    request: 1,
    stage: {
      id: 4,
      name: "Revise",
      description: "An edit to the draft was requested.",
      level: 4,
    },
    previousTransition: 8,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 10,
    request: 1,
    stage: {
      id: 1,
      name: "Draft",
      description: "A resource was created.",
      level: 1,
    },
    previousTransition: 9,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 11,
    request: 1,
    stage: {
      id: 2,
      name: "Submitted",
      description: "A resource was submitted",
      level: 2,
    },
    previousTransition: 10,
    created: new Date("2025-04-24T11:59:30.805896-04:00"),
  },
  {
    id: 12,
    request: 1,
    stage: {
      id: 5,
      name: "Rejected by Business Process Expert",
      description: "A resource was rejected by the Business Process Expert.",
      level: 5,
    },
    previousTransition: 11,
    created: new Date("2025-04-24T11:59:31.805896-04:00"),
  },
];
