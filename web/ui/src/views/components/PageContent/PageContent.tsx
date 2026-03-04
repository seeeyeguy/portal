import React from "react";

import styles from "views/components/PageContent/PageContent.module.css"

export interface IPageContentProps {
  className?: string;
  ariaDescription?: string;
  ref?: React.RefObject<HTMLDivElement> | undefined;
  children: React.ReactNode;
}

export default function PageContent({
  className = "",
  ariaDescription = "",
  ref = undefined,
  children,
}: IPageContentProps) {

  return (
    <div
      id="page-content"
      className={`${styles["page-content-margin"]} ${className}`}
      aria-description={ariaDescription}
      ref={ref}
    >
      {children}
    </div>
  );
}
