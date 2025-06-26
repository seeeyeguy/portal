import { redirect } from "react-router-dom";
import type { SearchBarMenuItem } from "adas-react-components/types";
import {
  faHome,
  faQuestion,
  faUserGear,
} from "@fortawesome/free-solid-svg-icons";

export default [
  {
    label: "Home",
    path: "/",
    icon: faHome,
    onClick: () => redirect("/"),
  },
  {
    label: "Admin",
    path: "/admin",
    icon: faUserGear,
    onClick: () => redirect("/admin"),
  },
  {
    label: "FAQ",
    path: "?faq=true",
    icon: faQuestion,
    onClick: () => {
      // Update url params.
      const searchParams = new URLSearchParams(window.location.search);
      searchParams.append("faq", "true");

      // Redirect to the URL with new params
      const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
      redirect(newUrl);
    },
  },
] as unknown as SearchBarMenuItem[];
