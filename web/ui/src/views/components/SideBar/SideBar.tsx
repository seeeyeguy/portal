import React from "react";
import {
  faAngleDown,
  faAngleRight,
  faArrowLeft,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { Menu } from "primereact/menu";
import { MenuItem } from "primereact/menuitem";

import styles from "views/components/SideBar/SideBar.module.css";

export interface IMenuLink {
  label: string;
  icon: JSX.Element;
  items: MenuItem[];
  customContent?: JSX.Element;
}

/** Properties for the SideBar component. */
export interface ISideBarProps {
  /** Header title of the side bar. */
  header: string;

  /** Menu values for the side bar. */
  menuLinks: IMenuLink[];

  /** ID of sibling container to add margin to sidebar. */
  siblingId?: string;
}

export default function SideBar({
  header,
  menuLinks,
  siblingId,
}: ISideBarProps) {
  const [expanded, setExpanded] = React.useState<boolean>(false);
  const [activeMenu, setActiveMenu] = React.useState<number | null>(null);
  const [animationDone, setAnimationDone] = React.useState<boolean>(false);

  React.useEffect(() => {
    // Add the sibling-margin class to the sibling container.
    const pageContent = document.getElementById(siblingId ?? "");
    if (pageContent) {
      pageContent.classList.add(styles["sibling-margin"]);
    }

    // Clean up on component unmount.
    return () => {
      if (pageContent) {
        pageContent.classList.remove(styles["sibling-margin"]);
      }
    };
  }, [siblingId]);

  const handleSubHeaderClick = React.useCallback(
    (index: number) => {
      setActiveMenu(activeMenu === index ? null : index);
      setExpanded(activeMenu !== index);

      // Prevents scrollbar stuttering when tranitioning menus.
      setTimeout(() => {
        setAnimationDone(lodash.isNumber(activeMenu === index ? null : index));
      }, 200);
    },
    [activeMenu]
  );

  const collapseAll = React.useCallback(() => {
    setActiveMenu(null);
    setExpanded(false);
  }, []);

  return (
    <>
      <nav
        className={`${styles["side-bar"]} ${expanded ? styles["side-bar-expanded"] : ""}`}
        aria-description="navigation side bar"
      >
        <header className={styles["side-bar-header"]}>
          <span
            aria-description="side bar header icon"
            className={`${styles["side-bar-header-icon"]} ${styles["side-bar-header-icon-open"]} ${expanded ? styles["hidden"] : ""}`}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              strokeWidth="2.5"
              viewBox="0 0 22 24"
              fill="none"
            >
              <path
                d="M6 11H19"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
              ></path>{" "}
              <path
                d="M15 5L21 11L15 17"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
              ></path>{" "}
              <path
                d="M1 1V21"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
              ></path>
            </svg>
          </span>
          <button
            className={`${styles["side-bar-header-icon"]} ${styles["side-bar-header-icon-collapse"]} ${!expanded ? styles["hidden"] : ""}`}
            aria-label="Collapse all"
            onClick={() => collapseAll()}
          >
            <FontAwesomeIcon icon={faArrowLeft} />
          </button>
          <h2 className={styles["side-bar-title"]}>{header}</h2>
        </header>
        <div
          className={styles["side-bar-content"]}
          aria-description="container for side bar menu links"
        >
          {menuLinks.map((mainLink, index) => (
            <section
              key={index}
              className={`${styles["side-bar-sub-header"]} ${index === activeMenu ? styles["expanded"] : ""} ${lodash.isNumber(activeMenu) && index !== activeMenu ? styles["hidden"] : ""}`}
            >
              <button
                className={styles["menu-header"]}
                onClick={() => handleSubHeaderClick(index)}
                aria-expanded={activeMenu === index}
                aria-controls={`menu-content-${index}`}
                aria-label={`Toggle ${mainLink.label} menu`}
              >
                <span
                  aria-description="menu header icon"
                  className={styles["menu-header-icon"]}
                >
                  {mainLink.icon}
                </span>
                <h3 className={styles["menu-header-label"]}>
                  {mainLink.label}
                </h3>
                <FontAwesomeIcon
                  className={styles["menu-header-arrow"]}
                  icon={expanded ? faAngleDown : faAngleRight}
                />
              </button>

              <div
                id={`menu-content-${index}`}
                className={`${styles["menu-content"]} ${activeMenu === index ? styles["expanded"] : ""} ${animationDone ? styles["scrollable"] : ""}`}
                aria-description="container for menu content"
              >
                <Menu className={styles["menu-items"]} model={mainLink.items} />
                {mainLink.customContent && (
                  <>
                    <hr />
                    {mainLink.customContent}
                  </>
                )}
              </div>
            </section>
          ))}
        </div>
      </nav>
      <div className={styles["side-bar-backdrop"]} />
    </>
  );
}
