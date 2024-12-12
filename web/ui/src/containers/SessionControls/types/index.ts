import React from "react";

import Tag from "state/types/portal/directory/Tag";

export interface SessionControlsProps {
  filterData: React.MutableRefObject<{
    [key: string]: string[];
  }>;
  filterTags: Tag[];
}
