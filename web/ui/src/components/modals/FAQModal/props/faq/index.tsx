import { faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { FAQ } from "components/modals/FAQModal/types";

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
  },
  {
    question: "How do I add/remove a resource to my favorites?",
    answer: (
      <>
        Hover and click the <FontAwesomeIcon icon={faStar} /> to add or remove a
        resource from your favorites.
      </>
    ),
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
  },
];
