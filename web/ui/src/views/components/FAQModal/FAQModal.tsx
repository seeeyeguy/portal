import React from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { FAQs, FAQ_CONTEXTS } from "views/components/FAQModal/FAQModalProps";

import styles from "views/components/FAQModal/FAQModal.module.css";

export interface IFAQModalProps {
  /** Optional context for FAQs to be displayed. */
  context?: string;
}

export default function FAQModal({
  context = FAQ_CONTEXTS.PORTAL,
}: IFAQModalProps) {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const faqModalRef = React.useRef<HTMLDialogElement | null>(null);

  React.useEffect(() => {
    if (faqModalRef.current) {
      if (searchParams?.get("faq")) {
        faqModalRef.current.showModal();
      } else {
        faqModalRef.current.close();
      }
    }
  }, [searchParams]);

  const handleClose = React.useCallback(() => {
    // Update url params.
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.delete("faq");

    // Redirect to the URL with new params
    const newUrl = `${window.location.pathname}?${searchParams.toString()}`;
    navigate(newUrl, { replace: true });
  }, [navigate]);

  const onClickClose = React.useCallback(
    (event: React.MouseEvent<HTMLElement>) => {
      const windowWidth = document.documentElement.clientWidth;
      const modalWidth = faqModalRef.current
        ? faqModalRef.current.clientWidth
        : 0;
      // Check if the mouse click was outside of the modal.
      if (faqModalRef.current && event.clientX < windowWidth - modalWidth) {
        handleClose();
      }
    },
    [faqModalRef, handleClose]
  );

  return (
    <dialog
      onClick={onClickClose}
      className={styles["faq-modal"]}
      ref={faqModalRef}
    >
      <header className={styles["faq-modal-header-row"]}>
        <h2>FAQ</h2>
        <button
          aria-description="faq modal close button"
          onClick={() => handleClose()}
        >
          <FontAwesomeIcon icon={faClose} size="lg" />
        </button>
      </header>
      <div
        className={styles["faq-modal-content"]}
        aria-description="container for frequently asked questions"
      >
        {(() => {
          const filteredFAQs = FAQs.filter((faq) =>
            faq.contexts.includes(context)
          );

          const categories = Array.from(
            new Set(filteredFAQs.map((faq) => faq.category || "No Category"))
          ).sort((a, b) =>
            a === "No Category" ? -1 : b === "No Category" ? 1 : 0
          );

          return categories.map((category, i) => (
            <div key={`category-${i}`}>
              {category !== "No Category" && <h3>{category}</h3>}
              {filteredFAQs
                .filter((faq) => (faq.category || "No Category") === category)
                .map((faq, j) => (
                  <details key={`faq-${i}-${j}`}>
                    <summary>{faq.question}</summary>
                    <p aria-description="faq answer">{faq.answer}</p>
                  </details>
                ))}
            </div>
          ));
        })()}
      </div>
    </dialog>
  );
}
