import { FileUploadFile } from "primereact/fileupload";

/**
 * Convert a Base64 string to File.
 * @param dataURL The string to convert.
 * @returns A File.
 */
export const base64ImageToFile = (dataURL?: string): File | null => {
  if (!dataURL) {
    return null;
  }
  // Extract the Base64 string from the data URL.
  const base64Index = dataURL.indexOf("base64,") + "base64,".length;
  const base64 = dataURL.substring(base64Index);

  // Decode the Base64 string to binary data.
  const binaryString = atob(base64);
  const binaryData = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    binaryData[i] = binaryString.charCodeAt(i);
  }

  // Get the MIME type from the data URL.
  const mimeTypeMatch = dataURL.match(/^data:(.*?);base64,/);
  if (!mimeTypeMatch) {
    throw new Error("Invalid data URL");
  }
  const mimeType = mimeTypeMatch[1];

  // Determine the file extension based on the MIME type.
  const extension = mimeType.split("/")[1];
  const fileName = `thumbnail.${extension}`;

  // Create a File object from the binary data.
  const file = new File([binaryData], fileName, { type: mimeType });

  return file;
};

/**
 * Convert a file to Base64.
 * @param file The file to convert.
 * @returns A Base64 string.
 */
export const fileUploadFileToBase64 = (
  file: FileUploadFile
): Promise<string> => {
  return fetch(file.objectURL)
    .then((response) => response.blob())
    .then((blob) => {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(blob);
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = (error) => reject(error);
      });
    });
};

/**
 * Convert a Base64 string to a FileUploadFile for FileUpload component.
 * @param string Base64 string to convert.
 * @returns A FileUploadFile.
 */
export const base64ToFileUploadFile = (dataURL: string): FileUploadFile => {
  // Extract the Base64 string from the data URL.
  const base64Index = dataURL.indexOf("base64,") + "base64,".length;
  const base64 = dataURL.substring(base64Index);

  // Decode the Base64 string to binary data.
  const binaryString = atob(base64);
  const binaryData = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    binaryData[i] = binaryString.charCodeAt(i);
  }

  // Get the MIME type from the data URL.
  const mimeTypeMatch = dataURL.match(/^data:(.*?);base64,/);
  if (!mimeTypeMatch) {
    throw new Error("Invalid data URL");
  }
  const mimeType = mimeTypeMatch[1];

  // Create a Blob from the binary data.
  const blob = new Blob([binaryData], { type: mimeType });

  // Create a File from the Blob.
  const file = new File([blob], "thumbnail", { type: mimeType });

  // Create a FileUploadFile object from the File
  const fileUploadFile = {
    name: file.name,
    size: file.size,
    type: file.type,
    objectURL: URL.createObjectURL(file),
  } as FileUploadFile;

  return fileUploadFile;
};

export const pathToFileUploadFile = (path: string): Promise<FileUploadFile> => {
  return fetch(path)
    .then((response) => response.blob())
    .then((blob) => {
      const file = new File([blob], "thumbnail.png", { type: blob.type });
      return {
        name: file.name,
        size: file.size,
        type: file.type,
        objectURL: URL.createObjectURL(file),
      } as FileUploadFile;
    });
};
