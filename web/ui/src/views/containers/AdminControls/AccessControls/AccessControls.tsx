import React from "react";
import { MultiValue } from "react-select";
import { MoonLoader } from "react-spinners";
import { LabelCheckboxSelect, SearchSelect } from "adas-react-components";
import { Option, OptionValues } from "adas-react-components/types";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import ConfirmModal from "views/components/ConfirmModal/ConfirmModal";

import { ISubFunction } from "definitions/portal/directory/SubFunction.types";
import { IAccess } from "definitions/portal/users/Access.types";

import { searchForEmployees } from "services/auth/ldapService";
import { useGetSubFunctionsQuery } from "state/query/api/portal/directory/SubFunctionApi";
import {
  TApiFetchAccessRequest,
  TApiPostAccessRequest,
  useAddAccessMutation,
  useGetAccessesQuery,
  useRevokeAccessMutation,
} from "state/query/api/portal/users/AccessApi";

import { ROLE_LEVELS } from "utils/PermissionUtility";
import { debounce } from "utils/PromiseUtility";
import { transformToOption } from "views/utils/OptionsUtility";

import styles from "views/containers/AdminControls/AccessControls/AccessControls.module.css";
import adminStyles from "views/containers/AdminControls/AdminControls.module.css";

type ReactSetStateHook = React.Dispatch<React.SetStateAction<Option[]>>;
/**
 * ACCESS CONSTANTS.
 */

const STAGE_LEVELS_FOR_ROLES = {
  [ROLE_LEVELS.DATA_STEWARD]: [],
  [ROLE_LEVELS.BUSINESS_PROCESS_EXPERT]: [2],
  [ROLE_LEVELS.SUPERUSER]: [2, 3],
};

/**
 *  ACCESS REQUEST PARAMS.
 */

const DEFAULT_ADD_ACCESS_PARAMS: TApiPostAccessRequest = {
  user: null,
  roleLevel: null,
  subfunctions: [],
  stageLevels: [],
};

const DEFAULT_QUERY_ACCESS_PARAMS: TApiFetchAccessRequest = {
  id: null,
  user: null,
  roleLevels: [],
  subfunctions: [],
  includeRevoked: null,
};

/**
 * OPTIONS FOR ROLE LEVEL SELECT FIELD.
 */

const ROLE_LEVELS_OPTIONS: Option[] = [
  transformToOption("Superuser", ROLE_LEVELS.SUPERUSER),
  transformToOption(
    "Business Process Expert",
    ROLE_LEVELS.BUSINESS_PROCESS_EXPERT
  ),
  transformToOption("Data Steward", ROLE_LEVELS.DATA_STEWARD),
];

export default function AccessControls() {
  /**************************
   * SHARED DEPENDENCIES.   *
   **************************/

  const [loadingUserFieldOptions, setLoadingUserFieldOptions] =
    React.useState<boolean>(false);

  const fetchUserOptions = React.useCallback(
    async (searchTerm: string) => {
      if (!searchTerm?.length) return [];
      setLoadingUserFieldOptions(true);
      let data = null;
      try {
        let modifiedSearchTerm = searchTerm;
        if (
          modifiedSearchTerm.includes(".") &&
          modifiedSearchTerm[0] !== "." &&
          !modifiedSearchTerm.includes("@")
        ) {
          const splitSearchTerm = modifiedSearchTerm.split(".");
          const [firstName, ...lastName] = splitSearchTerm;
          modifiedSearchTerm = firstName.trim();
          if (
            splitSearchTerm.length > 1 &&
            lastName?.length &&
            lastName[lastName.length - 1].trim()?.length
          ) {
            modifiedSearchTerm = `${modifiedSearchTerm} ${lastName[lastName.length - 1].trim()}`;
          }
        }
        data = await searchForEmployees(modifiedSearchTerm, 1, 25);
      } catch (err) {
        data = {};
      }
      setLoadingUserFieldOptions(false);
      return (data?.data ?? []).map((employee) =>
        transformToOption(employee.email)
      );
    },
    [setLoadingUserFieldOptions]
  );

  const debouncedFetchUserOptions = React.useMemo(
    () => debounce(fetchUserOptions, 500),
    [fetchUserOptions]
  );

  const loadAsyncUserFieldOptions = async (
    value: string
  ): Promise<Option[]> => {
    return debouncedFetchUserOptions(value);
  };

  const { data: subfunctionsQuery } = useGetSubFunctionsQuery(null);

  const subFunctionFieldOptions = React.useMemo(() => {
    const subfunctions = (subfunctionsQuery?.data ?? []) as ISubFunction[];
    return subfunctions.map((subfunction) =>
      transformToOption(
        `[${subfunction.function.name}] ${subfunction.name.includes("General::") ? "General" : subfunction.name}`,
        subfunction.id
      )
    );
  }, [subfunctionsQuery]);

  /********************************************
   * DEPENDENCIES FOR ACCESS FILTER CONTROLS. *
   ********************************************/

  const [filterUserFieldValue, setFilterUserFieldValue] =
    React.useState<OptionValues>(null);
  const [accessQueryParams, setAccessQueryParams] = React.useState(
    DEFAULT_QUERY_ACCESS_PARAMS
  );

  const onClearFilterUserField = React.useCallback(() => {
    setAccessQueryParams((s) => ({ ...s, user: null }));
  }, [setAccessQueryParams]);

  const onSubmitFilterUserField = React.useCallback(
    (searchTerm: string) => {
      setAccessQueryParams((s) => ({ ...s, user: searchTerm }));
    },
    [setAccessQueryParams]
  );

  const onChangeFilterAccessRecords = React.useCallback(
    (key: string) => (event: MultiValue<Option>) => {
      const values = (event ?? []).map((item) => item.value);
      setAccessQueryParams((s) => ({ ...s, [key]: values }));
    },
    [setAccessQueryParams]
  );

  /*******************************
   * DEPENDENCIES FOR MODALS.    *
   *******************************/

  /**
   *  DEPENDENCIES FOR ADD ACCESS MODAL.
   */
  const addModalRef = React.useRef<HTMLDialogElement>(null);
  const [addModalUserFieldValue, setAddModalUserFieldValue] =
    React.useState<OptionValues>(null);
  const [addAccessParams, setAddAccessParams] =
    React.useState<TApiPostAccessRequest>(DEFAULT_ADD_ACCESS_PARAMS);

  const [addAccessRecord] = useAddAccessMutation();

  const closeAddModal = React.useCallback(
    (event: React.MouseEvent) => {
      event.preventDefault();
      setAddAccessParams(DEFAULT_ADD_ACCESS_PARAMS);
      setAddModalUserFieldValue(null);
      setLoadingUserFieldOptions(false);
      addModalRef.current?.close();
    },
    [setAddAccessParams, setLoadingUserFieldOptions]
  );

  const showAddModal = React.useCallback(
    (event: React.MouseEvent) => {
      event.preventDefault();
      setAccessQueryParams(DEFAULT_QUERY_ACCESS_PARAMS);
      setFilterUserFieldValue(null);
      setLoadingUserFieldOptions(false);
      addModalRef.current?.showModal();
    },
    [setAccessQueryParams, setFilterUserFieldValue, setLoadingUserFieldOptions]
  );

  const onChangeAddField = React.useCallback(
    (key: string) => (event: MultiValue<Option>) => {
      const values = (event ?? []).map((item) => item.value) as number[];
      if (key === "roleLevel") {
        const value = values.splice(-1)?.[0];
        setAddAccessParams((s) => ({
          ...s,
          [key]: value,
          subfunctions: value === ROLE_LEVELS.SUPERUSER ? [] : s.subfunctions,
          stageLevels: STAGE_LEVELS_FOR_ROLES[value],
        }));
      } else {
        setAddAccessParams((s) => ({ ...s, [key]: values }));
      }
    },
    [setAddAccessParams]
  );

  const onClearAddUserField = React.useCallback(() => {
    setAddAccessParams((s) => ({ ...s, user: null }));
  }, [setAddAccessParams]);

  const onSubmitAddUserField = React.useCallback(
    (searchTerm: string) => {
      setAddAccessParams((s) => ({ ...s, user: searchTerm }));
    },
    [setAddAccessParams]
  );

  const onSubmitAddAccess = React.useCallback(
    (event: React.MouseEvent) => {
      event.preventDefault();
      addAccessRecord(addAccessParams);
      addModalRef.current?.close();
    },
    [addAccessParams, addAccessRecord]
  );

  /**
   * DEPENDENCIES FOR REVOKE ACCESS MODAL.
   */
  const [showRevokeModal, setShowRevokeModal] = React.useState(false);
  const [pendingRevokedRecord, setPendingRevokedRecord] =
    React.useState<IAccess | null>(null);

  const [revokeAccessRecord] = useRevokeAccessMutation();

  const onClickCancelRevokeAccess = React.useCallback(() => {
    setPendingRevokedRecord(null);
    setShowRevokeModal(false);
  }, [setPendingRevokedRecord, setShowRevokeModal]);

  const onClickConfirmRevokeAccess = React.useCallback(() => {
    if (pendingRevokedRecord?.id) {
      revokeAccessRecord(pendingRevokedRecord.id);
      setPendingRevokedRecord(null);
      setShowRevokeModal(false);
    }
  }, [
    pendingRevokedRecord,
    revokeAccessRecord,
    setPendingRevokedRecord,
    setShowRevokeModal,
  ]);

  const onSubmitRevokeAccess = React.useCallback(
    (accessRecord: IAccess) => () => {
      setPendingRevokedRecord(accessRecord);
      setShowRevokeModal(true);
    },
    [setPendingRevokedRecord, setShowRevokeModal]
  );

  /*************************
   *  RENDER COMPONENTS.   *
   *************************/

  const {
    data: accessQuery,
    isLoading,
    isFetching,
  } = useGetAccessesQuery(accessQueryParams);

  if (isLoading) {
    return (
      <div
        className={adminStyles["admin-loading"]}
        aria-description="container to display when loading initial data"
      >
        <MoonLoader />
      </div>
    );
  }

  const accesses = (accessQuery?.data ?? []) as IAccess[];

  return (
    <>
      <ConfirmModal
        open={showRevokeModal}
        title={`Revoking access for ${pendingRevokedRecord?.user?.email}?`}
        acceptLabel={<>Revoke</>}
        onReject={onClickCancelRevokeAccess}
        onAccept={onClickConfirmRevokeAccess}
        rejectClassName={`${adminStyles["admin-button"]} ${adminStyles["admin-button-cancel"]}`}
        acceptClassName={`${adminStyles["admin-button"]} ${adminStyles["admin-button-delete"]}`}
      />
      <dialog
        className={styles["access-add-controls-modal"]}
        onMouseDown={(event) => {
          if (event.target === event.currentTarget) {
            addModalRef.current?.close();
          }
        }}
        ref={addModalRef}
      >
        <form>
          <fieldset>
            <legend>Add Access</legend>
            <div
              className={styles["access-add-control-container"]}
              aria-description="add access control container"
            >
              <label
                htmlFor="search-select-user-add-control"
                className={styles["access-add-control-label"]}
              >
                User:
              </label>
              <SearchSelect
                id="search-select-user-add-control"
                options={loadAsyncUserFieldOptions}
                name="search-select-user-add-control"
                inputId="search-select-user-add-control"
                placeholder="Search..."
                values={addModalUserFieldValue}
                setValues={setAddModalUserFieldValue}
                onMenuOpen={() => null}
                loading={loadingUserFieldOptions}
                disabled={false}
                className={styles["access-add-control"]}
                onSubmitSelect={onSubmitAddUserField}
                onClearSelect={onClearAddUserField}
              />
            </div>
            <div
              className={styles["access-add-control-container"]}
              aria-description="add access control container"
            >
              <LabelCheckboxSelect
                id="multiselect-role-add-control"
                label="Role"
                options={ROLE_LEVELS_OPTIONS}
                name="multiselect-role-add-control"
                inputId="multiselect-role-add-control"
                values={ROLE_LEVELS_OPTIONS.filter(
                  (role) => role.value === addAccessParams?.roleLevel
                )}
                setValues={onChangeAddField("roleLevel") as ReactSetStateHook}
                horizontal={false}
                className={styles["access-add-control"]}
              />
            </div>
            <div
              className={styles["access-add-control-container"]}
              aria-description="add access control container"
            >
              <LabelCheckboxSelect
                id="multiselect-subfunctions-add-control"
                label="SubFunctions"
                options={subFunctionFieldOptions}
                name="multiselect-subfunctions-add-control"
                inputId="multiselect-subfunctions-add-control"
                values={subFunctionFieldOptions.filter((subfunction) =>
                  addAccessParams?.subfunctions?.includes(
                    subfunction.value as number
                  )
                )}
                setValues={
                  onChangeAddField("subfunctions") as ReactSetStateHook
                }
                disabled={addAccessParams.roleLevel === ROLE_LEVELS.SUPERUSER}
                horizontal={false}
                className={styles["access-add-control"]}
              />
            </div>
            <div className={styles["access-add-button-container"]}>
              <button
                onClick={closeAddModal}
                className={styles["access-add-button-cancel"]}
              >
                Cancel
              </button>
              <button
                type="submit"
                onClick={onSubmitAddAccess}
                disabled={!(addAccessParams.user && addAccessParams.roleLevel)}
                className={styles["access-add-button-submit"]}
              >
                Grant
              </button>
            </div>
          </fieldset>
        </form>
      </dialog>
      <section>
        <button
          className={styles["access-add-controls-modal-button"]}
          onClick={showAddModal}
        >
          <FontAwesomeIcon icon={faPlus} />
          Add Access
        </button>
      </section>
      <section>
        <form>
          <div
            className={styles["access-filter-controls"]}
            aria-description="filter controls container"
          >
            <div aria-description="user filter control container">
              <label
                htmlFor="search-select-user-filter-control"
                className={styles["access-filter-control-label"]}
              >
                User:
              </label>
              <SearchSelect
                id="search-select-user-filter-control"
                options={loadAsyncUserFieldOptions}
                name="search-select-user-filter-control"
                inputId="search-select-user-filter-control"
                placeholder="Search..."
                values={filterUserFieldValue}
                setValues={setFilterUserFieldValue}
                onMenuOpen={() => null}
                loading={loadingUserFieldOptions}
                disabled={false}
                className={styles["access-filter-control"]}
                onSubmitSelect={onSubmitFilterUserField}
                onClearSelect={onClearFilterUserField}
              />
            </div>
            <LabelCheckboxSelect
              id="multiselect-roles-filter-control"
              label="Roles"
              options={ROLE_LEVELS_OPTIONS}
              name="multiselect-roles-filter-control"
              inputId="multiselect-roles-filter-control"
              values={ROLE_LEVELS_OPTIONS.filter((role) =>
                accessQueryParams?.roleLevels?.includes(role.value as number)
              )}
              setValues={
                onChangeFilterAccessRecords("roleLevels") as ReactSetStateHook
              }
              horizontal={false}
              className={styles["access-filter-control"]}
            />
            <LabelCheckboxSelect
              id="multiselect-subfunctions-filter-control"
              label="SubFunctions"
              options={subFunctionFieldOptions}
              name="multiselect-subfunctions-filter-control"
              inputId="multiselect-subfunctions-filter-control"
              values={subFunctionFieldOptions.filter((subfunction) =>
                accessQueryParams?.subfunctions?.includes(
                  subfunction.value as number
                )
              )}
              setValues={
                onChangeFilterAccessRecords("subfunctions") as ReactSetStateHook
              }
              horizontal={false}
              className={styles["access-filter-control"]}
            />
          </div>
        </form>
      </section>
      <section>
        {!isFetching && !accesses?.length ? (
          <p className={adminStyles["admin-loading"]}>No Accesses Found</p>
        ) : (
          <>
            <h3>Access Records</h3>
            <ul className={styles["access-records-list"]}>
              {accesses.map((access) => (
                <li key={access.id}>
                  <article>
                    <div aria-description="access record container">
                      <p>{access.user.email}</p>
                      <p>{access.role.name}</p>
                      <p>
                        {(access.subfunctions as ISubFunction[])
                          .map(
                            (subfunction) =>
                              `[${subfunction.function.name}] ${subfunction.name.includes("General::") ? "General" : subfunction.name}`
                          )
                          .join(", ")}
                      </p>
                    </div>
                    <div
                      className={styles["access-revoke-button-container"]}
                      aria-description="access revoke button container"
                    >
                      <button
                        className={styles["access-revoke-button"]}
                        onClick={onSubmitRevokeAccess(access)}
                      >
                        Revoke
                      </button>
                    </div>
                  </article>
                </li>
              ))}
            </ul>
          </>
        )}
      </section>
    </>
  );
}
