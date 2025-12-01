import { faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { FAQ } from "views/definitions/FAQModal.types";

export const FAQ_CONTEXTS = {
  PORTAL: "portal",
  PRT: "prt",
  PPR: "ppr",
};

export const FAQs: FAQ[] = [
  {
    question:
      "Why don't I have access to a certain link?  How can I request access?",
    answer: (
      <>
        We don't control, manage, or grant access to any tool or system link
        through The Portal. Permissions for all resources are managed through
        the native system. Please contact the POC found on the hover pop-up for
        each resource or utilize the source system to request and gain access.
        <br></br>
        <br></br>Certain links on The Portal are restricted based on job
        function and/or role. Please consider whether you need access to a
        resource before submitting an access request.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PORTAL],
  },
  {
    question: "How do I request a new Tableau account?",
    answer: (
      <>
        A Tableau account can be requested by submitting a{" "}
        <a
          href="https://l3harris.servicenowservices.com/sp?id=sc_cat_item&table=sc_cat_item&sys_id=9ff18fecdb6a841017cdf2821f961905"
          target="_blank"
        >
          “Tableau Access Request”
        </a>{" "}
        ticket in ONEHub.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PORTAL],
  },
  {
    question: "How do I add/remove a resource to my favorites?",
    answer: (
      <>
        Hover and click the <FontAwesomeIcon icon={faStar} /> to add or remove a
        resource from your favorites.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PORTAL],
  },
  {
    question:
      "Who should I contact regarding questions about content shown on The Portal?",
    answer: (
      <>
        For questions related to content, please reach out to the point of
        contact listed for each resource. The point of contact can be found in
        the tooltip that appears when you hover over a resource.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PORTAL],
  },
  {
    question:
      "What is the Program Performance Reporting (PPR) tool used for and which programs are required to input data?",
    answer: (
      <>
        Each period, Tier 1 and Tier 2 programs are required to report their
        performance data to CHQ. The Program Performance Reporting (PPR) tool
        streamlines this process by automatically collecting data from
        PeopleSoft and Cobra, helping reduce reporting time for program teams.
        <br />
        <br />
        Each program is responsible for completing the subjective assessment and
        entering any data that cannot be automatically pulled from source
        systems.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PPR],
  },
  {
    question: "How do I manage my program team?",
    answer: (
      <>
        The program team is populated directly from the Support Team Members
        listed in PeopleSoft. Any necessary updates should be made in
        PeopleSoft.
        <br />
        <br />
        Team member information in the Program Performance Reporting tool is
        refreshed daily at 3 a.m., 11 a.m., and 3 p.m. to reflect any changes
        made in the system.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PPR],
  },
  {
    question:
      "When is data for program team member assignments in PeopleSoft updated?",
    answer: (
      <>
        If you make changes to program team member assignments, you will see
        those changes reflected in our system at 5 a.m., 1 p.m., and 5 p.m.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PPR],
  },
  {
    question: "Why isn't my Project ID available in the tool?",
    answer: (
      <>
        Access to program data is managed utilizing the program team in
        PeopleSoft. If you are unable to access your assigned Tier 1 or Tier 2
        programs, please review the Program Team Members in PeopleSoft to ensure
        the program team information is accurate.
        <br />
        <br />
        Team member information in the Program Performance Reporting tool is
        refreshed daily at 3 a.m., 11 a.m., and 3 p.m. to reflect any changes
        made in the system.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PPR],
  },
  {
    question: "How do I view data submitted for prior reporting periods?",
    answer: (
      <>
        The Reporting Period filter allows programs teams to view data submitted
        in the prior reporting period. For additional periods, please utilize
        the Program Performance report in the
        <br />
        <a href="https://app.high.powerbigov.us/groups/me/apps/ac2afc6b-21b6-4e6f-8676-598620024698/reports/fc05f2a9-2782-4972-a5f8-179fb7aa9b23/8581b61c07df049490e9">
          Power BI Program Management app
        </a>
        .
      </>
    ),
    contexts: [FAQ_CONTEXTS.PPR],
  },
  {
    question: `Why was my program identified as a "Red Program"?`,
    answer: (
      <>
        Programs are identified as "Red Programs" if they meet one or more of
        the following criteria:
        <ol>
          <li>{"CPI < 0.9"}</li>
          <li>{"SPI < 0.9"}</li>
          <li>EAC Growth (EAC is greater than BAC by 10% or more)</li>
          <li>Over Target Cost (EAC is greater than Contract Value)</li>
          <li>Red Overall Program Subjective Assessment</li>
        </ol>
        Hovering over the "Red Program" badge will present a tooltip with the
        specific conditions that marked the program as a red program.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PPR],
  },
  {
    question: "Who should I contact regarding technical difficulties?",
    answer: (
      <>
        If you are experiencing technical difficulties with The Portal, please
        contact{" "}
        <a href="mailto:SAS-Portal@L3Harris.com">SAS-Portal@L3Harris.com</a>.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PORTAL, FAQ_CONTEXTS.PPR],
  },
  {
    question:
      "Who selected the resources that are included in The Portal?  Why don't I see a certain resource?",
    answer: (
      <>
        Each functional Data Owner curated the list of standard resources for
        their function. The Portal doesn’t contain all possible resources, but
        rather those that have been identified as key content by each function.
        <br />
        <br />
        Please note that resources will be reviewed and updated regularly to
        ensure the site content remains comprehensive and accurate.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PORTAL],
  },
  {
    category: "General",
    question:
      "Where can I find additional information about the Program Review Tool (PRT)?",
    answer: (
      <>
        Additional information can be found on the SAS PMX Business Intelligence
        SharePoint site:{" "}
        <a href="https://connect.l3harris.com/sites/sas-pgm-mgmt/PRT/SitePages/PM-BUSINESS-INTELLIGENCE-TOOLS.aspx">
          PMX BI Tools
        </a>
        .
      </>
    ),
    contexts: [FAQ_CONTEXTS.PRT],
  },
  {
    category: "Errors/Issues",
    question: `What should I do if I receive a “Request timed out” error?`,
    answer: (
      <>
        The PRT generation service relies on connectivity to certain internal
        resources that may occasionally be unavailable. Please wait 15 minutes
        and try again. If the service remains unavailable, please contact:{" "}
        <a href="mailto:SAS-Portal@L3Harris.com">SAS-Portal@L3Harris.com</a>.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PRT],
  },
  {
    category: "Errors/Issues",
    question:
      "Why am I receiving a “Portfolio generation service unavailable, please try again later” error?”",
    answer: (
      <>
        The PRT generation service relies on connectivity to the Tableau API,
        which may occasionally experience degraded performance or temporary
        outages. Please wait 15 minutes before retrying slide generation. If the
        issue persists, please contact:{" "}
        <a href="mailto:SAS-Portal@L3Harris.com">SAS-Portal@L3Harris.com</a>.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PRT],
  },
  {
    category: "Errors/Issues",
    question:
      "Who should I contact if I am having other technical difficulties not listed in the FAQ?",
    answer: (
      <>
        Please contact:{" "}
        <a href="mailto:SAS-Portal@L3Harris.com">SAS-Portal@L3Harris.com</a>.
        Include a description of what occurred, any error messages, and
        screenshots if available.
      </>
    ),
    contexts: [FAQ_CONTEXTS.PRT],
  },
];
