import React from "react";
import { MoonLoader } from "react-spinners";
import { toast } from "react-toastify";
import { faPlus, faCopy } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import lodash from "lodash";
import FormType from "@rjsf/core";
import Form from "@rjsf/primereact";
import validator from "@rjsf/validator-ajv8";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";
import FormCard from "views/components/FormCard/FormCard";

import { DEFAULT_API_ERROR_MESSAGE } from "definitions/ApiConstants";

import {
  MaintenanceBannerFormData,
  maintenanceBannerSchema,
  maintenanceBannerUiSchema,
} from "views/schemas/administration/MaintenanceBannersSchema";

import {
  MAINTENANCE_BANNERS_CONTENT_KEY,
  useGetContentQuery,
  useAddContentMutation,
  useUpdateContentMutation,
  useRemoveContentMutation,
} from "state/query/api/portal/content/ContentApi";

import { IContent } from "definitions/portal/content/Content.types";
import { IAuthUser } from "definitions/Sso.types";

import { resolveApiErrorMessage } from "utils/PromiseUtility";

import styles from "views/containers/AdminControls/AdminControls.module.css";

type RouteTypes = (
  | {
      path: string;
      element: JSX.Element;
      loader: () => Promise<
        | Response
        | {
            user: Response | IAuthUser;
          }
      >;
      children?: undefined;
    }
  | {
      path: string;
      children: (
        | {
            index: boolean;
            element: JSX.Element;
            loader: () => Promise<
              | Response
              | {
                  user: Response | IAuthUser;
                }
            >;
            path?: undefined;
          }
        | {
            path: string;
            element: JSX.Element;
            loader: () => Promise<
              | Response
              | {
                  user: Response | IAuthUser;
                }
            >;
            index?: undefined;
          }
        | {
            path: string;
            loader: () => Response;
            index?: undefined;
            element?: undefined;
          }
      )[];
      element?: undefined;
      loader?: undefined;
    }
)[];

export default function MaintenanceBannerControls() {
  const { data: resp, isLoading } = useGetContentQuery(
    MAINTENANCE_BANNERS_CONTENT_KEY
  );
  const maintenanceBanners = resp?.data as IContent | undefined;
  const bannerData = maintenanceBanners?.content as unknown as
    | Record<string, MaintenanceBannerFormData>
    | undefined;

  const [selectedMaintenanceBanner, setSelectedMaintenanceBanner] =
    React.useState<MaintenanceBannerFormData | null>(null);

  const [addContent] = useAddContentMutation();
  const [updateContent] = useUpdateContentMutation();
  const [removeContent] = useRemoveContentMutation();

  const [showAddModal, setShowAddModal] = React.useState(false);
  const [showCloneModal, setShowCloneModal] = React.useState(false);
  const [showDeleteModal, setShowDeleteModal] = React.useState(false);
  const [showUpdateModal, setShowUpdateModal] = React.useState(false);

  const newFormRef = React.useRef<FormType>(null);
  const [newFormKey, setNewFormKey] = React.useState(Date.now());

  const [cloneFormData, setCloneFormData] =
    React.useState<MaintenanceBannerFormData | null>(null);
  const cloneFormRef = React.useRef<FormType>(null);
  const [cloneFormKey, setCloneFormKey] = React.useState(Date.now());

  const [schemaForAdd, setSchemaForAdd] = React.useState<
    typeof maintenanceBannerSchema
  >(lodash.cloneDeep(maintenanceBannerSchema));
  const [schemaForClone, setSchemaForClone] = React.useState<
    typeof maintenanceBannerSchema
  >(lodash.cloneDeep(maintenanceBannerSchema));
  const [schemaForUpdate, setSchemaForUpdate] = React.useState<
    typeof maintenanceBannerSchema
  >(lodash.cloneDeep(maintenanceBannerSchema));

  React.useEffect(() => {
    // Needed to avoid a circular dependency
    // by dynamically importing the routes to get the
    // site paths for the maintenance banner page field.
    import("routes/index").then((module) => {
      const routes = module.ROUTES as RouteTypes;
      const sitePaths = routes.reduce((acc, route) => {
        if (route.path === "*") {
          return acc;
        }
        if (route.children) {
          return [
            ...acc,
            ...route.children.reduce((acc, child) => {
              if (child.index) {
                return acc;
              }
              return [...acc, `${route.path}/${child.path}`];
            }, [] as string[]),
          ];
        }
        return [...acc, route.path];
      }, [] as string[]);
      setSchemaForUpdate((s) => ({
        ...s,
        properties: {
          ...s.properties,
          page: {
            ...((s?.properties?.page as object) ?? {}),
            oneOf: sitePaths.map((path) => ({ const: path, title: path })),
          },
        },
      }));
    });
  }, []);

  React.useEffect(() => {
    // Needed to avoid a circular dependency
    // by dynamically importing the routes to get the
    // site paths for the maintenance banner page field.
    import("routes/index").then((module) => {
      const routes = module.ROUTES as RouteTypes;
      const sitePaths = routes.reduce((acc, route) => {
        if (route.path === "*") {
          return acc;
        }
        if (route.children) {
          return [
            ...acc,
            ...route.children.reduce((acc, child) => {
              if (child.index) {
                return acc;
              }
              return [...acc, `${route.path}/${child.path}`];
            }, [] as string[]),
          ];
        }
        return [...acc, route.path];
      }, [] as string[]);
      setSchemaForAdd((s) => ({
        ...s,
        properties: {
          ...s.properties,
          page: {
            ...((s?.properties?.page as object) ?? {}),
            oneOf: [
              { const: null, title: "Select Page" },
              ...sitePaths.reduce(
                (acc, path) => {
                  if (lodash.has(bannerData, path)) {
                    return acc;
                  }
                  return [...acc, { const: path, title: path }];
                },
                [] as { const: string; title: string }[]
              ),
            ],
          },
        },
      }));
    });
  }, [bannerData]);

  React.useEffect(() => {
    // Needed to avoid a circular dependency
    // by dynamically importing the routes to get the
    // site paths for the maintenance banner page field.
    import("routes/index").then((module) => {
      const routes = module.ROUTES as RouteTypes;
      const sitePaths = routes.reduce((acc, route) => {
        if (route.path === "*") {
          return acc;
        }
        if (route.children) {
          return [
            ...acc,
            ...route.children.reduce((acc, child) => {
              if (child.index) {
                return acc;
              }
              return [...acc, `${route.path}/${child.path}`];
            }, [] as string[]),
          ];
        }
        return [...acc, route.path];
      }, [] as string[]);
      setSchemaForClone((s) => ({
        ...s,
        properties: {
          ...s.properties,
          page: {
            ...((s?.properties?.page as object) ?? {}),
            oneOf: [
              { const: null, title: "Select Page" },
              ...sitePaths.reduce(
                (acc, path) => {
                  if (lodash.has(bannerData, path)) {
                    return acc;
                  }
                  return [...acc, { const: path, title: path }];
                },
                [] as { const: string; title: string }[]
              ),
            ],
          },
          clone: {
            ...((s?.properties?.clone as object) ?? {}),
            oneOf: [
              { const: null, title: "Select Page" },
              ...Object.keys(bannerData ?? {}).map((key) => ({
                const: key,
                title: key,
              })),
            ],
          },
          level: {
            ...((s?.properties?.level as object) ?? {}),
            oneOf: [
              { const: null, title: "Select Clone" },
              ...((s?.properties?.level as Record<string, object[]>)?.oneOf ?? []),
            ],
          },
        },
      }));
    });
  }, [bannerData]);

  const handleCreate = React.useCallback(async () => {
    if (newFormRef.current && newFormRef.current.validateForm()) {
      const formSubmission: MaintenanceBannerFormData = {
        ...newFormRef.current.state.formData,
      };

      // Create request body.
      const body = {
        key: MAINTENANCE_BANNERS_CONTENT_KEY,
        content: {},
      };

      if (lodash.has(formSubmission, "clone")) {
        delete formSubmission.clone;
      }

      let response;
      if (lodash.isEmpty(bannerData ?? {})) {
        body.content = {
          [formSubmission.page]: formSubmission,
        };
        response = await addContent(body);
      } else {
        body.content = {
          ...(bannerData ?? {}),
          [formSubmission.page]: formSubmission,
        };
        response = await updateContent({
          key: MAINTENANCE_BANNERS_CONTENT_KEY,
          body: { content: body.content },
        });
      }

      // Handle the create API error.
      if (response.error) {
        const message =
          "data" in response.error
            ? resolveApiErrorMessage(response.error.data as string | object)
            : DEFAULT_API_ERROR_MESSAGE;

        toast.error(`Error creating maintenance banner: ${message}`);
      } else {
        toast.success("Maintenance Banner Created");
        // Reset form on success.
        setShowAddModal(false);
        setNewFormKey(Date.now());
      }
    }
  }, [bannerData, addContent, setShowAddModal, setNewFormKey, updateContent]);

  const handleClone = React.useCallback(async () => {
    cloneFormRef.current?.setState((s) => ({ ...s, formData: cloneFormData }));
    if (cloneFormRef.current && cloneFormRef.current.validateForm()) {
      const formSubmission: MaintenanceBannerFormData = {
        ...cloneFormRef.current.state.formData,
      };

      // Create request body.
      const body = {
        key: MAINTENANCE_BANNERS_CONTENT_KEY,
        content: {},
      };

      if (lodash.has(formSubmission, "clone")) {
        delete formSubmission.clone;
      }

      body.content = {
        ...(bannerData ?? {}),
        [formSubmission.page]: formSubmission,
      };
      await updateContent({
        key: MAINTENANCE_BANNERS_CONTENT_KEY,
        body: { content: body.content },
      })
        .unwrap()
        .then(() => toast.success("Maintenance Banner Created."))
        .catch((error) => toast.error(error.data));

      // Reset form on success.
      setShowCloneModal(false);
      setCloneFormKey(Date.now());
    }
  }, [bannerData, cloneFormData, updateContent, setShowCloneModal]);

  const handleCloneFormChange = React.useCallback(
    ({ formData }: { formData: MaintenanceBannerFormData }) => {
      setCloneFormData(formData);
      if (!lodash.isEmpty(formData?.clone)) {
        if (maintenanceBanners && !lodash.isEmpty(bannerData)) {
          const bannerKeyToClone = formData.clone as string;
          const bannerToClone = bannerData[bannerKeyToClone];
          if (bannerToClone) {
            setCloneFormData({
              ...formData,
              level: bannerToClone.level,
              header: bannerToClone.header,
              body: bannerToClone.body,
              subtext: bannerToClone.subtext,
            });
          }
        }
      } else {
        setCloneFormData(null);
      }
    },
    [bannerData, maintenanceBanners, setCloneFormData]
  );

  // Clear new maintenance banner form to empty.
  const handleCancel = React.useCallback(() => {
    setShowAddModal(false);
    setNewFormKey(Date.now());
  }, []);

  const handleCancelClone = React.useCallback(() => {
    setCloneFormData(null);
    setShowCloneModal(false);
    setCloneFormKey(Date.now());
  }, []);

  const handleDeleteMaintenanceBanner = React.useCallback(async () => {
    if (selectedMaintenanceBanner) {
      const body = {
        content: {
          ...bannerData,
        },
      };
      delete body.content[selectedMaintenanceBanner.page];

      if (lodash.isEmpty(body.content)) {
        removeContent(MAINTENANCE_BANNERS_CONTENT_KEY)
          .unwrap()
          .then(() => toast.success("Deleted Maintenance Banner."))
          .catch((error) => toast.error(error.data));
      } else {
        updateContent({ key: MAINTENANCE_BANNERS_CONTENT_KEY, body })
          .unwrap()
          .then(() => toast.success("Deleted Maintenance Banner."))
          .catch((error) => toast.error(error.data));
      }

      setSelectedMaintenanceBanner(null);
      setShowDeleteModal(false);
    }
  }, [
    bannerData,
    selectedMaintenanceBanner,
    removeContent,
    setSelectedMaintenanceBanner,
    setShowDeleteModal,
    updateContent,
  ]);

  const handleUpdateMaintenanceBanner = React.useCallback(async () => {
    if (selectedMaintenanceBanner) {
      const formData = {
        ...selectedMaintenanceBanner,
      };

      if (lodash.has(formData, "clone")) {
        delete formData.clone;
      }

      updateContent({
        body: {
          content: {
            ...bannerData,
            [formData.page]: formData,
          },
        },
        key: MAINTENANCE_BANNERS_CONTENT_KEY,
      })
        .unwrap()
        .then(() => toast.success("Updated Maintenance Banner."))
        .catch((error) => toast.error(error.data));

      setShowUpdateModal(false);
      setSelectedMaintenanceBanner(null);
    }
  }, [
    bannerData,
    selectedMaintenanceBanner,
    setSelectedMaintenanceBanner,
    setShowUpdateModal,
    updateContent,
  ]);

  const handleUpdateModalCancel = React.useCallback(() => {
    setSelectedMaintenanceBanner(null);
    setShowUpdateModal(false);
  }, [setSelectedMaintenanceBanner, setShowUpdateModal]);

  return (
    <>
      <div
        className={styles["admin-controls"]}
        aria-description="container to maintenance banner controls"
      >
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          onClick={() => setShowAddModal(true)}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Maintenance Banner
        </button>
        <button
          className={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
          disabled={lodash.isEmpty(bannerData ?? {})}
          onClick={() => setShowCloneModal(true)}
        >
          <FontAwesomeIcon icon={faCopy} />
          Clone Maintenance Banner
        </button>
      </div>
      {isLoading ? (
        <div
          className={styles["admin-loading"]}
          aria-description="container to display when loading initial data"
        >
          <MoonLoader />
        </div>
      ) : (
        <div
          className={styles["card-list"]}
          aria-description="container for list of maintenance banners"
        >
          {!maintenanceBanners && <p>No maintenance banners found.</p>}
          <ul>
            {(
              Object.values(
                bannerData ?? {}
              ) as unknown as MaintenanceBannerFormData[]
            ).map((banner) => (
              <li key={banner.page}>
                <FormCard
                  formProps={{
                    schema: schemaForUpdate,
                    uiSchema: {
                      ...maintenanceBannerUiSchema,
                      page: {
                        ...maintenanceBannerUiSchema.page,
                        "ui:disabled": true,
                      },
                    },
                    formData: {
                      ...banner,
                      page: banner.page,
                    },
                    validator: validator,
                  }}
                  onDelete={() => {
                    setSelectedMaintenanceBanner({ ...banner });
                    setShowDeleteModal(true);
                  }}
                  onSubmit={(e) => {
                    setSelectedMaintenanceBanner({
                      ...banner,
                      ...e?.formData,
                    });
                    setShowUpdateModal(true);
                  }}
                />
              </li>
            ))}
          </ul>
        </div>
      )}
      <ConfirmModal
        title={"Add Maintenance Banner"}
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
          validator={validator}
          schema={schemaForAdd}
          uiSchema={maintenanceBannerUiSchema}
          showErrorList={false}
          noHtml5Validate={true}
        />
      </ConfirmModal>
      <ConfirmModal
        title={"Clone Maintenance Banner"}
        open={showCloneModal}
        acceptLabel={<>Clone</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleClone()}
        onReject={() => handleCancelClone()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-submit"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
        className={styles["new-modal-form"]}
      >
        <Form
          key={cloneFormKey}
          ref={cloneFormRef}
          formData={cloneFormData}
          validator={validator}
          schema={schemaForClone}
          uiSchema={{
            ...maintenanceBannerUiSchema,
            clone: {
              ...maintenanceBannerUiSchema.clone,
              "ui:widget": "select",
            },
            level: {
              ...maintenanceBannerUiSchema.level,
              "ui:disabled": true,
            },
            header: {
              ...maintenanceBannerUiSchema.header,
              "ui:disabled": true,
            },
            body: {
              ...maintenanceBannerUiSchema.body,
              "ui:disabled": true,
            },
            subtext: {
              ...maintenanceBannerUiSchema.subtext,
              "ui:disabled": true,
            },
          }}
          showErrorList={false}
          noHtml5Validate={true}
          onChange={(event) =>
            handleCloneFormChange(
              event as typeof event & { formData: MaintenanceBannerFormData }
            )
          }
        />
      </ConfirmModal>
      <ConfirmModal
        title="Update Maintenance Banner"
        open={showUpdateModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Update</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleUpdateMaintenanceBanner()}
        onReject={() => handleUpdateModalCancel()}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-save"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
      <ConfirmModal
        title="Delete Maintenance Banner"
        open={showDeleteModal}
        className={styles["formcard-modal"]}
        acceptLabel={<>Delete</>}
        rejectLabel={<>Cancel</>}
        onAccept={() => handleDeleteMaintenanceBanner()}
        onReject={() => setShowDeleteModal(false)}
        acceptClassName={`${styles["admin-button"]} ${styles["admin-button-delete"]}`}
        rejectClassName={`${styles["admin-button"]} ${styles["admin-button-cancel"]}`}
      />
    </>
  );
}
