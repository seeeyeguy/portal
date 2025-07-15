import React from "react";
import { toast } from "react-toastify";
import { WidgetProps } from "@rjsf/utils";
import { v4 as uuidv4 } from "uuid";

import {
  FileUpload,
  FileUploadHeaderTemplateOptions,
  FileUploadSelectEvent,
  FileUploadUploadEvent,
} from "primereact/fileupload";
import { Tooltip } from "primereact/tooltip";

import {
  fileUploadFileToBase64,
  pathToFileUploadFile,
} from "views/utils/ImageUtility";

import styles from "views/components/FileUploadWidget/FileUploadWidget.module.css";

/** Properties for the UpDownWidget component. */
export interface FileUploadWidgetProps extends WidgetProps {
  /** Extended options for the file input. */
  options: {
    /** File types that are allowed. */
    accept?: string;

    /** Max file size in Bytes for the uploaded file. */
    maxFileSize: number;
  };
}

/**
 * FileUploadWidget component for React JSON Schema Form.
 * This widget uses PrimeReact's FileUpload component to handle form files.
 */
export default function FileUploadWidget({
  value,
  options,
  disabled,
  onChange,
}: WidgetProps) {
  // Destructure options and avoid passing invalid options to the DOM element.
  const {
    accept = "image/png, image/jpeg, image/jpg",
    maxFileSize = 5242880, // 5 MegaBytes.
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    enumOptions,
    ...restOptions
  } = options || {};

  const [totalSize, setTotalSize] = React.useState(0);
  const [chooseIconID] = React.useState(`id-${uuidv4()}`);
  const [clearIconID] = React.useState(`id-${uuidv4()}`);

  const fileUploadRef = React.useRef<FileUpload>(null);

  // Upload previously provided thumbnail to input.
  React.useEffect(() => {
    if (value && fileUploadRef.current) {
      // Check if type is of FileUploadFile.
      if (value.objectURL) {
        setTotalSize(value.size);
        fileUploadRef.current.setFiles([value]);
        fileUploadFileToBase64(value).then((convertedFile) =>
          onChange(convertedFile)
        );
      } else if (typeof value === "string") {
        // Assume value is a path.
        pathToFileUploadFile(value).then((newFile) => {
          if (fileUploadRef.current) {
            setTotalSize(newFile.size);
            fileUploadRef.current.setFiles([newFile]);
            fileUploadFileToBase64(newFile).then((convertedFile) =>
              onChange(convertedFile)
            );
          }
        });
      }
    }
  }, [value, onChange]);

  const handleFileEvent = React.useCallback(
    (event: FileUploadSelectEvent | FileUploadUploadEvent) => {
      const acceptedTypes = accept
        .split(",")
        .map((type: string) => type.trim());
      let invalidFiles = false;
      let _totalSize = 0;

      // Check if the file is valid.
      event.files.forEach((file: File) => {
        if (!acceptedTypes.includes(file.type)) {
          invalidFiles = true;
        }
        _totalSize += file.size || 0;
      });

      if (invalidFiles) {
        toast.error(
          `File type not supported. Supported types include: ${acceptedTypes}`
        );
        fileUploadRef.current?.clear();
        return;
      }

      setTotalSize(_totalSize);
      fileUploadFileToBase64(event.files[0]).then((convertedFile) =>
        onChange(convertedFile)
      );
    },
    [accept, onChange]
  );

  // Clear file input.
  const handleFileClear = React.useCallback(() => {
    setTotalSize(0);

    onChange(undefined);
  }, [onChange]);

  const headerTemplate = React.useCallback(
    (options: FileUploadHeaderTemplateOptions) => {
      const { className, chooseButton, cancelButton } = options;
      const formattedValue =
        fileUploadRef && fileUploadRef.current
          ? fileUploadRef.current.formatSize(totalSize)
          : "0 B";

      return (
        <div
          className={`${className} ${styles["header"]}`}
          aria-description="container for a file upload header"
        >
          {chooseButton}
          {cancelButton}
          <span
            className={styles["file-size"]}
            aria-description="uploaded file size"
          >
            {`${formattedValue} / ${(maxFileSize / (1025 * 1025)).toFixed(1)} MB`}
          </span>
        </div>
      );
    },
    [fileUploadRef, maxFileSize, totalSize]
  );

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const itemTemplate = (file: any) => {
    return (
      <div
        className={styles["file-item"]}
        aria-description="uploaded file preview"
      >
        <img alt={file.name} role="presentation" src={file.objectURL} />
      </div>
    );
  };

  const emptyTemplate = React.useCallback(() => {
    return (
      <div
        className={styles["file-item"]}
        aria-description="empty file container"
      >
        <i className={`pi pi-image mt-3 p-5 ${styles["image-icon"]}`}></i>
        <span className={styles["drag-drop-text"]}>
          Drag and Drop Image Here
        </span>
      </div>
    );
  }, []);

  const chooseFileIcon = React.useMemo(
    () => ({
      icon: "pi pi-fw pi-images",
      iconOnly: true,
      className: `${chooseIconID} p-button-rounded p-button-outlined`,
    }),
    [chooseIconID]
  );

  const clearFileIcon = React.useMemo(
    () => ({
      icon: "pi pi-fw pi-times",
      iconOnly: true,
      className: `${clearIconID} p-button-danger p-button-rounded p-button-outlined`,
    }),
    [clearIconID]
  );

  return (
    <div
      className={styles["file-upload-widget"]}
      aria-description="container for a file upload widget"
    >
      <Tooltip
        target={`.${chooseIconID}`}
        content="Browse for a file."
        position="bottom"
      />
      <Tooltip
        target={`.${clearIconID}`}
        content="Clear current file."
        position="bottom"
      />

      <FileUpload
        disabled={disabled}
        ref={fileUploadRef}
        url="/api/upload"
        accept={accept}
        maxFileSize={maxFileSize}
        onUpload={handleFileEvent}
        onSelect={handleFileEvent}
        onError={handleFileClear}
        onClear={handleFileClear}
        headerTemplate={headerTemplate}
        itemTemplate={itemTemplate}
        emptyTemplate={emptyTemplate}
        chooseOptions={chooseFileIcon}
        cancelOptions={clearFileIcon}
        {...restOptions}
      />
    </div>
  );
}
