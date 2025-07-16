import React from "react";
import { faPlusSquare, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import { Dropdown, DropdownChangeEvent } from "primereact/dropdown";
import { WidgetProps } from "@rjsf/utils";

import { ITag } from "definitions/portal/directory/Tag.types";

import { ITagDecomposed, parseTags } from "views/utils/TagUtility";

import styles from "views/components/TagSelectionWidget/TagSelectionWidget.module.css";

// Dropdown options.
interface SelectOption {
  label?: string;
  value: string | number;
}

/** Properties for the UpDownWidget component. */
export interface TagSelectionWidgetProps extends WidgetProps {
  /** Extended options for tag selection. */
  options: {
    /** Array of tags to be added as options. */
    tags: ITag[];
  };
}

/**
 * UpDownWidget component for React JSON Schema Form.
 * This widget decomposed tag labels into individual filtering and selectable elements.
 */
export default function TagSelectionWidget({
  value,
  options,
  disabled,
  onChange,
}: WidgetProps) {
  // Destructure tags out of options.
  const { tags } = options || {};

  const decomposedTags = parseTags(tags);

  const [selectedCategory, setSelectedCategory] = React.useState<string | null>(
    null
  );
  const [selectedSubCategory, setSelectedSubCategory] = React.useState<
    string | null
  >(null);
  const [selectedTags, setSelectedTags] = React.useState<ITagDecomposed[]>(
    parseTags(tags).filter((tag: ITagDecomposed) => value.includes(tag.id))
  );

  // Categories to show in the options.
  const visibleCategories: SelectOption[] = React.useMemo(() => {
    const categoryMap = decomposedTags.reduce((acc, tag) => {
      // If the category is truthy, add it to the map.
      if (tag.category) {
        acc.set(tag.category, {
          label: tag.category,
          value: tag.category,
        });
      }
      return acc;
    }, new Map<string, SelectOption>());
    return Array.from(categoryMap.values());
  }, [decomposedTags]);

  // Filtered subcategories to show in the options.
  const visibleSubCategories: SelectOption[] = React.useMemo(() => {
    const subcategoryMap = decomposedTags.reduce((acc, tag) => {
      // If the tag's category matches the selected category and subcategory is truthy.
      if (tag.category === selectedCategory && tag.subcategory) {
        acc.set(tag.subcategory, {
          label: tag.subcategory,
          value: tag.subcategory,
        });
      }
      return acc;
    }, new Map<string, SelectOption>());

    return Array.from(subcategoryMap.values());
  }, [decomposedTags, selectedCategory]);

  // Filtered tags to show in the options.
  const visibleTags: SelectOption[] = React.useMemo(
    () =>
      decomposedTags.reduce((acc, tag) => {
        // If a category is selected and the tag's category does not match the selected category, exclude the tag.
        if (selectedCategory && tag.category !== selectedCategory) {
          return acc;
        }

        // If a subcategory is selected and the tag's subcategory does not match the selected subcategory, exclude the tag.
        if (selectedSubCategory && tag.subcategory !== selectedSubCategory) {
          return acc;
        }

        // Exclude tags that are already in the selectedTags array.
        if (selectedTags.some((selectedTag) => selectedTag.id === tag.id)) {
          return acc;
        }

        // Add the tag to the accumulator.
        acc.push({
          label: `${tag.tagName} (${tag.label})`,
          value: tag.id,
        });

        return acc;
      }, [] as SelectOption[]),
    [decomposedTags, selectedCategory, selectedSubCategory, selectedTags]
  );

  // Currently selected tag, not yet added to the selected tag list.
  const [currentTag, setCurrentTag] = React.useState<number | null>(null);

  React.useEffect(() => {
    onChange(selectedTags.map((tag) => tag.id));
  }, [selectedTags, onChange]);

  // Recalculate filters for sub-categories and tags on category change.
  const handleCategoryChange = (event: DropdownChangeEvent) => {
    // Reset tag dropdown.
    setCurrentTag(null);

    setSelectedCategory(event.value || null);
    setSelectedSubCategory(null);
  };

  // Recalculate filters for tags on sub-category change.
  const handleSubCategoryChange = (event: DropdownChangeEvent) => {
    // Reset tag dropdowns.
    setCurrentTag(null);
    setSelectedSubCategory(event.value);
  };

  // Remove tag from selected tags list.
  const handleRemoveTag = (id: number) => {
    setSelectedTags((prev: ITagDecomposed[]) => {
      const newTags = prev.filter((tag) => tag.id !== id);
      return newTags;
    });
  };

  // Add tag to selected tags list.
  const handleAddTag = React.useCallback(() => {
    const newTag = decomposedTags.find((tag) => tag.id === currentTag);

    if (newTag) {
      setSelectedTags((prev: ITagDecomposed[]) => {
        const newTags = [newTag, ...prev];
        return newTags;
      });
      // Reset tag dropdown.
      setCurrentTag(null);
    }
  }, [currentTag, decomposedTags]);

  return (
    <div
      className={styles["tag-widget"]}
      aria-description="container for a tag widget"
    >
      <div
        className={styles["category-selection"]}
        aria-description="container for category and sub-category dropdowns"
      >
        <Dropdown
          appendTo="self"
          disabled={disabled}
          value={selectedCategory}
          options={visibleCategories}
          onChange={handleCategoryChange}
          placeholder="Select Category"
          showClear
        />

        <Dropdown
          appendTo="self"
          value={selectedSubCategory}
          options={visibleSubCategories}
          disabled={disabled || lodash.isEmpty(visibleSubCategories)}
          onChange={handleSubCategoryChange}
          placeholder="Select Sub-Category"
        />
      </div>
      <div
        className={styles["tag-selection"]}
        aria-description="container for tag dropdown"
      >
        <Dropdown
          appendTo="self"
          disabled={disabled}
          value={currentTag}
          options={visibleTags}
          onChange={(event: DropdownChangeEvent) => setCurrentTag(event.value)}
          filter
          placeholder="Select Tag"
          virtualScrollerOptions={{
            itemSize: 32,
          }}
        />
        <button
          className={styles["tag-add-button"]}
          disabled={lodash.isNull(currentTag)}
          onClick={handleAddTag}
          aria-label="add tag"
        >
          <FontAwesomeIcon
            icon={faPlusSquare}
            className={styles["tag-add-icon"]}
          />
        </button>
      </div>
      <div aria-description="container for selected tags">
        <p>Selected Tags</p>
        <ul className={styles["selected-tags"]}>
          {selectedTags?.map((tag) => (
            <li key={tag.id}>
              <span aria-description="container for tag label">
                <b>{tag.tagName}</b>
                {` (${tag.label})`}
              </span>
              <button
                disabled={disabled}
                className={styles["tag-delete-button"]}
                onClick={() => handleRemoveTag(tag.id)}
                aria-label="remove tag"
              >
                <FontAwesomeIcon
                  className={styles["tag-delete-icon"]}
                  icon={faTrash}
                />
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
