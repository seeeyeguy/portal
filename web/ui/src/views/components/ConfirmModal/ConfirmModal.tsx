import React, { ReactNode } from "react";
import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "views/components/ConfirmModal/ConfirmModal.module.css";

/** Properties for the ConfirmModal component. */
interface IConfirmModalProps {
  /** Show or not to show the dialog box. */
  open?: boolean;

  /** Title of the component. */
  title?: string;

  /** Main content of the component. */
  children?: ReactNode;

  /** Class selector for the component content. */
  className?: string;

  /** Label for the `Accept` button. */
  acceptLabel?: JSX.Element;

  /** Label for the `Reject` button. */
  rejectLabel?: JSX.Element;

  /** Label for the `Alternative` button. */
  alternativeLabel?: JSX.Element;

  /** Class selector for the `Accept` button component. */
  acceptClassName?: string;

  /** Class selector for the `Reject` button component. */
  rejectClassName?: string;

  /** Class selector for the `Alternative` button component. */
  alternativeClassName?: string;

  /** Callback to invoke when the `Accept` button is clicked. */
  onAccept?: () => Promise<void> | void;

  /** Callback to invoke when the `Reject` button is clicked. */
  onReject?: () => Promise<void> | void; 

  /** Callback to invoke when the dialog box is hidden. */
  onHide?: (() => void) | null;

  /** Callback to invoke when the `Alternative` button is clicked. */
  onAlternative?: () => Promise<void> | void;
}

export default function ConfirmModal({
  open,
  title = "Continue?",
  children,
  className = "",
  acceptLabel,
  rejectLabel,
  alternativeLabel,
  acceptClassName = "",
  rejectClassName = "",
  alternativeClassName = "",
  onAccept,
  onReject,
  onHide = null,
  onAlternative,
}: IConfirmModalProps) {
  const handleAlternative = React.useCallback(async () => {
    if (onAlternative) {
      await onAlternative();
    }
  }, [onAlternative]);

  const handleAccept = React.useCallback(async () => {
    if (onAccept) {
      await onAccept();
    }
  }, [onAccept]);

  const handleClickOutside = (
    event: React.MouseEvent<HTMLDialogElement, MouseEvent>
  ) => {
    if (event.target === event.currentTarget) {
      handleHide();
    }
  };

  const handleHide = React.useCallback(async () => {
    if (onHide) {
      onHide();
    } else if (onReject) {
      await onReject();
    }
  }, [onHide, onReject]);

  const handleReject = React.useCallback(async () => {
    if (onReject) {
      await onReject();
    }
  }, [onReject]);

  const showFooter = acceptLabel || rejectLabel || alternativeLabel;

  return (
    <dialog
      open={open}
      className={styles["confirm-modal"]}
      onMouseDown={handleClickOutside}
    >
      <section className={`${styles["modal-content"]} ${className}`}>
        <button
          className={styles["close"]}
          onClick={handleHide}
          aria-label="close"
        >
          <FontAwesomeIcon icon={faClose} />
        </button>
        <header>
          <h3>{title}</h3>
        </header>
        <main>{children}</main>
        {showFooter && (
          <footer>
            {rejectLabel && (
              <button
                type="button"
                className={`${styles["cancel-button"]} ${rejectClassName}`}
                onClick={handleReject}
              >
                {rejectLabel}
              </button>
            )}
            {alternativeLabel && (
              <button
                type="button"
                className={`${styles["alternative-button"]} ${alternativeClassName}`}
                onClick={handleAlternative}
              >
                {alternativeLabel}
              </button>
            )}
            {acceptLabel && (
              <button
                type="button"
                className={`${styles["confirm-button"]} ${acceptClassName}`}
                onClick={handleAccept}
              >
                {acceptLabel}
              </button>
            )}
          </footer>
        )}
      </section>
    </dialog>
  );
}
