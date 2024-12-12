import React from "react";

export interface LoadSessionButtonProps {
  filterData: React.MutableRefObject<{
    [key: string]: string[];
  }>;
  className: string;
}
