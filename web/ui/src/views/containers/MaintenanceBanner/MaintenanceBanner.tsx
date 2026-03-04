import MaintenanceBannerComponent, {
  LogLevels,
} from "views/components/MaintenanceBanner/MaintenanceBanner";

import { MaintenanceBannerFormData } from "views/schemas/administration/MaintenanceBannersSchema";

import {
  MAINTENANCE_BANNERS_CONTENT_KEY,
  useGetContentQuery,
} from "state/query/api/portal/content/ContentApi";

import { IContent } from "definitions/portal/content/Content.types";

export default function MaintenanceBanner({
  page,
}: {
  page: string;
}) {
  const { data: resp } = useGetContentQuery(MAINTENANCE_BANNERS_CONTENT_KEY);
  const maintenanceBanners = resp?.data as IContent | undefined;
  const bannerData = (
    maintenanceBanners?.content as unknown as
      | Record<string, MaintenanceBannerFormData>
      | undefined
  )?.[page];

  if (!bannerData) {
    return <></>;
  }

  const { level, header, body, subtext, enabled, dismissable } = bannerData;

  return (
    <MaintenanceBannerComponent
      level={level as unknown as LogLevels}
      header={header}
      body={body}
      subtext={subtext}
      enabled={enabled}
      dismissable={dismissable}
    />
  );
}
