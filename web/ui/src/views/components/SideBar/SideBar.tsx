import React from "react";
import { redirect, useLocation } from "react-router-dom";
import {
  faAngleDown,
  faAngleRight,
  faArrowLeft,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { Menu } from "primereact/menu";
import { MenuItem, MenuItemCommandEvent } from "primereact/menuitem";

import styles from "views/components/SideBar/SideBar.module.css";

export interface IMenuLink {
  label: string;
  icon: JSX.Element;
  path: string | null;
  customContent?: JSX.Element;
  items?: MenuItem[];
  url?: string;
  visible?: boolean;
  command?(event: MenuItemCommandEvent): void;
}

/** Properties for the SideBar component. */
export interface ISideBarProps {
  /** Header title of the side bar. */
  header: string;

  /** Menu values for the side bar. */
  menuLinks: IMenuLink[];
}

export default function SideBar({
  header,
  menuLinks,
}: ISideBarProps) {
  const location = useLocation();

  const [expanded, setExpanded] = React.useState<boolean>(false);
  const [activeMenu, setActiveMenu] = React.useState<number | null>(null);
  const [animationDone, setAnimationDone] = React.useState<boolean>(false);
  const [closed, setClosed] = React.useState<boolean>(false);

  React.useLayoutEffect(() => {
    const recomputeNavBarHeightProperty = () => {
      // Query the visible navbar from the DOM.
      const navBarElements = document.querySelectorAll(
        'nav[class*="search-bar-container"]'
      );
      const visibleNavBarElement = Array.from(navBarElements).filter(
        (element) => element.clientHeight > 0
      )?.[0];

      if (visibleNavBarElement) {
        // Get the computed position of the bottom of the
        // navbar relative to the viewport.
        const computedHeight = Math.ceil(
          visibleNavBarElement.getBoundingClientRect().bottom
        );

        // Set the navbar height dynamically.
        const root = document.documentElement;
        // --nav-bar-height used to help position the sidebar.
        root.style.setProperty("--nav-bar-height", `${computedHeight}px`);
      }
    };

    const targetNode = document.getElementById("root");

    if (!targetNode) {
      return;
    }

    const callback = (mutationsList: MutationRecord[]) => {
      for (const mutation of mutationsList) {
        if (mutation.type === "childList" || mutation.type === "attributes") {
          recomputeNavBarHeightProperty();
        }
      }
    };

    const observer = new MutationObserver(callback);
    const config = { childList: true, subtree: true, attributes: true };
    observer.observe(targetNode, config);

    return () => observer.disconnect();

  }, []);

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

  const closeSidebar = React.useCallback(() => {
    // Force close sidebar.
    setTimeout(() => {
      setClosed(true);
      collapseAll();
    }, 200);

    // Allow sidebar to open.
    setTimeout(() => {
      setClosed(false);
    }, 800);
  }, [collapseAll]);

  const processMenuLinks = (
    links: IMenuLink[] | MenuItem[]
  ): IMenuLink[] | MenuItem[] => {
    return links.map((link) => {
      const originalCommand = link.command;

      link.command = (event: MenuItemCommandEvent) => {
        if (originalCommand) {
          originalCommand(event);
        }
        closeSidebar();
      };

      if (link.items) {
        link.items = processMenuLinks(link.items as MenuItem[]);
      }

      return link;
    });
  };

  const processedMenuLinks = processMenuLinks(menuLinks);

  return (
    <>
      <nav
        className={`${styles["side-bar"]} ${closed ? styles["side-bar-closed"] : ""} ${expanded ? styles["side-bar-expanded"] : ""}`}
        aria-description="navigation side bar"
      >
        <header className={styles["side-bar-header"]}>
          <span
            className={`${styles["side-bar-header-icon"]} ${styles["side-bar-header-icon-open"]} ${expanded ? styles["hidden"] : ""}`}
            aria-description="side bar header icon"
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
            onClick={() => collapseAll()}
            aria-label="Collapse all"
          >
            <FontAwesomeIcon icon={faArrowLeft} />
          </button>
          <h2 className={styles["side-bar-title"]}>{header}</h2>
        </header>
        <div
          className={styles["side-bar-content"]}
          aria-description="container for side bar menu links"
        >
          {(processedMenuLinks as IMenuLink[]).map((mainLink, index) => {
            const items: MenuItem[] =
              mainLink.items?.map((menuLink) => ({
                ...menuLink,
                className:
                  location.pathname === menuLink.data?.path
                    ? styles["selected-item"]
                    : "",
              })) ?? [];

            const isSelected =
              (items.some((item) => location.pathname === item.data?.path) ||
                location.pathname === mainLink.path) &&
              index !== activeMenu;

            // Split to allow handling of headers with and without children differently.
            return (mainLink.url ?? mainLink.command) &&
              !mainLink.items &&
              mainLink.visible !== false ? (
              <section
                key={index}
                className={`${styles["side-bar-sub-header"]} ${index === activeMenu ? styles["expanded"] : ""} ${lodash.isNumber(activeMenu) && index !== activeMenu ? styles["hidden"] : ""}`}
              >
                <button
                  className={`${styles["menu-header"]} ${isSelected ? styles["selected-item"] : ""}`}
                  onClick={(e) => {
                    e.preventDefault();
                    if (mainLink.command) {
                      mainLink.command({ originalEvent: e, item: mainLink });
                    } else if (mainLink.url) {
                      redirect(mainLink.url);
                    }
                  }}
                  aria-label={`${mainLink.label} menu item`}
                >
                  <span
                    className={styles["menu-header-icon"]}
                    aria-description="menu header icon"
                  >
                    {mainLink.icon}
                  </span>
                  <h3 className={styles["menu-header-label"]}>
                    {mainLink.label}
                  </h3>
                </button>
              </section>
            ) : (
              mainLink.visible !== false && (
                <section
                  key={index}
                  className={`${styles["side-bar-sub-header"]} ${index === activeMenu ? styles["expanded"] : ""} ${lodash.isNumber(activeMenu) && index !== activeMenu ? styles["hidden"] : ""}`}
                >
                  <button
                    className={`${styles["menu-header"]} ${isSelected ? styles["selected-item"] : ""}`}
                    onClick={() => handleSubHeaderClick(index)}
                    aria-expanded={activeMenu === index}
                    aria-controls={`menu-content-${index}`}
                    aria-label={`Toggle ${mainLink.label} menu`}
                  >
                    <span
                      className={styles["menu-header-icon"]}
                      aria-description="menu header icon"
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
                    <Menu className={styles["menu-items"]} model={items} />
                    {mainLink.customContent && (
                      <>
                        <hr />
                        {mainLink.customContent}
                      </>
                    )}
                  </div>
                </section>
              )
            );
          })}
        </div>
      </nav>
      <div className={styles["side-bar-backdrop"]} />
    </>
  );
}
