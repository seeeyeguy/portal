import React from "react";
import { useLoaderData } from "react-router";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import lodash from "lodash";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { AutoComplete } from "primereact/autocomplete";
import { Paginator, PaginatorPageChangeEvent } from "primereact/paginator";
import FormType from "@rjsf/core";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import FormCard from "views/components/FormCard/FormCard";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";
import { ITag } from "definitions/portal/directory/Tag.types";
import { IAuthUser } from "definitions/Sso.types";

import {
  TagFormData,
  tagSchema,
  tagUiSchema,
  tagCustomValidate,
} from "views/schemas/administration/TagSchema";

import {
  TApiPostTagRequest,
  TApiPutTagRequest,
  useAddTagMutation,
  useGetTagsQuery,
  useRemoveTagMutation,
  useSearchTagsQuery,
  useUpdateTagMutation,
} from "state/query/api/portal/directory/TagApi";

import { hasSuperuserPermissions } from "utils/PermissionUtility";
import { resolveApiErrorMessage } from "utils/PromiseUtility";
import { parseTags } from "views/utils/TagUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";

const convertToTagLabel = (tagSubmission: TagFormData): string => {
  let tagLabel = "";

  if (tagSubmission.category && tagSubmission.subcategory) {
    tagLabel = `${tagSubmission.category}::${tagSubmission.subcategory}:${tagSubmission.name}`;
  } else {
    tagLabel = tagSubmission.name;
  }

  return tagLabel;
};

export default function TagControls() {
  const loaderData = useLoaderData() as { user: IAuthUser };

  const superuserPermissions = React.useMemo(
    () => hasSuperuserPermissions(loaderData.user),
    [loaderData]
  );

  const { data: tags, isLoading } = useGetTagsQuery(null);

  const [addTag] = useAddTagMutation();
  const [updateTag] = useUpdateTagMutation();
  const [removeTag] = useRemoveTagMutation();

  const [showAddModal, setShowAddModal] = React.useState(false);
  const [showUpdateModal, setShowUpdateModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);

  const [tempFormData, setTempFormData] = React.useState<TagFormData | null>(
    null
  );
  const [tempFormId, setTempFormId] = React.useState<number | null>(null);

  const newFormRef = React.useRef<FormType>(null);
  const [newFormKey, setNewFormKey] = React.useState(Date.now());

  // Pagination State.
  const [page, setPage] = React.useState(0);
  const [rows, setRows] = React.useState(5);
  const [totalRows, setTotalRows] = React.useState(0);

  // Pagination State Updates.
  const onPageChange = (event: PaginatorPageChangeEvent) => {
    setPage(event.first);
    setRows(event.rows);
  };

  // What the user typed.
  const [search, setSearch] = React.useState("");
  // What the user searched.
  const [debouncedSearch, setDebouncedSearch] = React.useState("");

  const [filteredTags, setFilteredTags] = React.useState<string[]>([]);

  // Debounced search.
  const handleDebouncedChange = React.useMemo(() => {
    const debouncedFunction = lodash.debounce(
      (searchText: string) => {
        setDebouncedSearch(searchText);
        setPage(0);
      },
      200,
      {
        leading: true,
      }
    );

    // Return a function that calls the debounced function
    return (searchText: string) => {
      debouncedFunction(searchText);
    };
  }, []);

  // Load searched tags.
  const { data: searchTags, isFetching } = useSearchTagsQuery(debouncedSearch);

  // All tags decomposed.
  const decomposedTags = React.useMemo(
    () => (tags?.data ? parseTags(tags.data as ITag[]) : []),
    [tags]
  );

  // Searched tags decomposed, separated from the decomposedTags
  // since those are needed for creating unique categories.
  const decomposedSearchTags = React.useMemo(
    () => (searchTags?.data ? parseTags(searchTags.data as ITag[]) : []),
    [searchTags]
  );

  // Tags that are being displayed.
  const displayedTags = React.useMemo(() => {
    const retrievedTags = search ? decomposedSearchTags : decomposedTags;

    setTotalRows(retrievedTags.length);
    return retrievedTags.slice(page, page + rows);
  }, [decomposedSearchTags, decomposedTags, page, rows, search]);

  // Unique category options.
  const categories = React.useMemo(
    () =>
      decomposedTags.reduce((acc: string[], tag) => {
        if (tag.category && !acc.includes(tag.category)) {
          acc.push(tag.category);
        }
        return acc;
      }, []) ?? [],
    [decomposedTags]
  );

  // Unique subcategory options.
  const subCategories = React.useMemo(
    () =>
      decomposedTags.reduce((acc: string[], tag) => {
        if (tag.subcategory && !acc.includes(tag.subcategory)) {
          acc.push(tag.subcategory);
        }
        return acc;
      }, []) ?? [],
    [decomposedTags]
  );

  // Autocomplete search handling.
  const handleFilter = React.useCallback(
    (filterEvent: { query: string }) => {
      const query = filterEvent.query.toLowerCase();
      setFilteredTags(
        ((searchTags?.data || []) as ITag[]).reduce(
          (acc: string[], tag: ITag) => {
            if (tag.label.toLowerCase().includes(query)) {
              acc.push(tag.label);
            }
            return acc;
          },
          []
        )
      );
    },
    [searchTags]
  );

  // Schema Options.
  const updatedSchema = React.useMemo(() => {
    if (categories || subCategories) {
      return {
        ...tagSchema,
        properties: {
          ...tagSchema.properties,
          category: {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            ...(tagSchema.properties?.category as any),
            ...(superuserPermissions
              ? { examples: categories }
              : {
                  oneOf: [
                    { const: "", title: "Select Category" },
                    ...categories.map((value) => ({
                      const: value,
                      title: value,
                    })),
                  ],
                }),
          },
          subcategory: {
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            ...(tagSchema.properties?.subcategory as any),
            examples: subCategories,
          },
        },
      };
    }
    return tagSchema;
  }, [categories, subCategories, superuserPermissions]);

  const updatedUiSchema = React.useMemo(() => {
    if (categories && subCategories) {
      return {
        ...tagUiSchema,
        category: {
          ...tagUiSchema?.category,
          "ui:widget": superuserPermissions ? "text" : "select",
        },
        "ui:submitButtonOptions": {
          norender: true,
        },
      };
    }
  }, [categories, subCategories, superuserPermissions]);

  const handleCreate = React.useCallback(async () => {
    if (newFormRef.current && newFormRef.current.validateForm()) {
      const formSubmission: TagFormData = {
        ...newFormRef.current.state.formData,
      };

      // Create request body.
      const body: TApiPostTagRequest = {
        label: convertToTagLabel(formSubmission),
      };

      const response = await addTag(body);

      // Handle the create API error.
      if (response.error) {
        const message =
          "data" in response.error
            ? resolveApiErrorMessage(response.error.data as string | object)
            : DEFAULT_API_ERROR_MESSAGE;

        toast.error(`Error creating tag: ${message}`);
      } else {
        toast.success(`Tag Created`);
        // Reset form on success.
        setShowAddModal(false);
        setNewFormKey(Date.now());
      }
    }
  }, [addTag]);

  // Clear new tag form to empty.
  const handleCancel = React.useCallback(() => {
    setShowAddModal(false);
    setNewFormKey(Date.now());
  }, []);

  const handleUpdate = React.useCallback(
    async (id: number | null, submittedData: TagFormData | null) => {
      if (id && submittedData) {
        const formSubmission: TagFormData = {
          ...submittedData,
        };

        // update request body.
        const body: TApiPutTagRequest = {
          label: convertToTagLabel(formSubmission),
        };

        const response = await updateTag({ body, id });

        // Handle the update API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          toast.error(`Error updating tag:${message}`);
        } else {
          toast.success(`Tag Updated`);
          // Reset form on success.
          setShowUpdateModal(false);
          setTempFormData(null);
          setTempFormId(null);
        }
      }
    },
    [updateTag]
  );

  const handleDelete = React.useCallback(
    async (id: number | null) => {
      if (id) {
        const response = await removeTag(id);

        // Handle the delete API error.
        if (response.error) {
          const message =
            "data" in response.error
              ? resolveApiErrorMessage(response.error.data as string | object)
              : DEFAULT_API_ERROR_MESSAGE;

          toast.error(`Error deleting tag: ${message}`);
        } else {
          toast.success(`Tag Deleted`);
          // Reset form on success.
          setShowDeleteModal(false);
          setTempFormId(null);
        }
      }
    },
    [removeTag]
  );

  return (
    <>
      <div
        className={styles["admin-controls"]}
        aria-description="container to tag controls"
      >
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowAddModal(true)}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Tag
        </button>
        <AutoComplete
          className={styles["admin-search"]}
          placeholder="Search Tags/Categories"
          value={search}
          suggestions={filteredTags}
          onChange={(event) => {
            handleDebouncedChange(event.value ?? "");
            setSearch(event.value ?? "");
          }}
          dropdown
          completeMethod={handleFilter}
          showEmptyMessage={true}
        />
        <Paginator
          className={styles["admin-paginator"]}
          first={page}
          rows={rows}
          totalRecords={totalRows}
          rowsPerPageOptions={[5, 10, 20]}
          onPageChange={onPageChange}
        />
        {isFetching && (
          <div
            className={styles["admin-filter-loading"]}
            aria-description="container to display when loading data with filters"
          >
            <MoonLoader size={30} />
          </div>
        )}
      </div>
      {isLoading ? (
        <div
          className={styles["admin-loading"]}
          aria-description="container to display when loading initial data"
        >
          <MoonLoader />
        </div>
      ) : search && !isFetching && searchTags?.data.length === 0 ? (
        <p className={styles["admin-loading"]}>No Tags Found</p>
      ) : (
        <div
          className={styles["card-list"]}
          aria-description="container for list of tags"
        >
          <ul>
            {displayedTags.map((tag) => (
              <li key={tag.id}>
                <FormCard
                  key={tag.id}
                  formProps={{
                    formData: {
                      name: tag.tagName,
                      category: tag.category ?? "",
                      subcategory: tag.subcategory ?? "",
                    },
                    schema: updatedSchema,
                    uiSchema: updatedUiSchema,
                    validator: validator,
                    customValidate: tagCustomValidate,
                  }}
                  onDelete={() => {
                    setTempFormData(null);
                    setTempFormId(tag.id);
                    setShowDeleteModal(true);
                  }}
                  onSubmit={(submittedData) => {
                    setTempFormData(submittedData?.formData);
                    setTempFormId(tag.id);
                    setShowUpdateModal(true);
                  }}
                />
              </li>
            ))}
          </ul>
        </div>
      )}
      <ConfirmModal
        title={"Update Tag"}
        open={showUpdateModal}
        acceptLabel={<>Update</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleUpdate(tempFormId, tempFormData)}
        onReject={() => setShowUpdateModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
      <ConfirmModal
        title={"Delete Tag"}
        open={showDeleteModal}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleDelete(tempFormId)}
        onReject={() => setShowDeleteModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />

      <ConfirmModal
        title={"Add Tag"}
        open={showAddModal}
        acceptLabel={<>Add</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleCreate()}
        onReject={() => handleCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
        className={styles["new-modal-form"]}
      >
        <Form
          key={newFormKey}
          ref={newFormRef}
          schema={updatedSchema}
          uiSchema={updatedUiSchema}
          validator={validator}
          customValidate={tagCustomValidate}
          showErrorList={false}
          noHtml5Validate={true}
        />
      </ConfirmModal>
    </>
  );
}
