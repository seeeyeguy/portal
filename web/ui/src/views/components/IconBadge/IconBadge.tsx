import { Badge } from "primereact/badge";

import styles from "views/components/IconBadge/IconBadge.module.css";

export interface IIconBadgeProps {
  icon: React.ReactNode;
  badgeValue?: string | null;
  badgeClassName?: string;
}

export default function IconBadge({
  icon,
  badgeValue = " ",
  badgeClassName,
}: IIconBadgeProps) {
  return (
    <div 
      className={styles["icon-wrapper"]}
      aria-description="container for icon and its badge"
    >
      {icon}
      {badgeValue && (
        <Badge
          className={`${styles["icon-badge"]} ${badgeClassName ? badgeClassName : ""} `}
          value={badgeValue}
        />
      )}
    </div>
  );
}
