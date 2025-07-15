import { ITag } from "definitions/portal/directory/Tag.types";

// Decomposed to provide options for dropdowns.
export interface ITagDecomposed extends ITag {
  category?: string | null;
  subcategory?: string | null;
  tagName: string;
}

/**
 * Decomposes a string tag into its base components and adds the
 * properties to an extended tag object.
 * @param tags Array of tags.
 * @returns Decomposed Tags.
 */
export const parseTags = (tags: ITag[] = []): ITagDecomposed[] => {
  return tags.map((item) => {
    const [category, rest] = item.label.split("::");
    const [subcategory, tag] = rest ? rest.split(":") : [null, category];

    return {
      ...item,
      category: rest ? category : null,
      subcategory: rest ? subcategory : null,
      tagName: tag,
    };
  });
};
