import { redirect } from "react-router-dom";
import type { SearchBarMenuItem } from "adas-react-components/types";
import { faHome, faQuestion } from "@fortawesome/free-solid-svg-icons";

export default [
  {
    label: "Home",
    path: "/",
    icon: faHome,
    onClick: () => redirect("/"),
  },
  {
    label: "FAQ",
    path: "/",
    icon: faQuestion,
    onClick: () => redirect("/"),
  },
] as unknown as SearchBarMenuItem[];
