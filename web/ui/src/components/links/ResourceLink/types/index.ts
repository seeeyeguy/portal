export interface ResourceLinkProps {
  id: number;
  name: string;
  description: string;
  url: string;
  thumbnail: string;
  primaryPointOfContact: string;
  download: boolean;
  favoriteId?: number | null | undefined;
}
