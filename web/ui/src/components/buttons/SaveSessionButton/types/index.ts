import React from "react";

import Tag from "state/types/portal/directory/Tag";

export interface SaveSessionButtonProps {
  filterData: React.MutableRefObject<{
    [key: string]: string[];
  }>;
  filterTags: Tag[];
  className: string;
}
