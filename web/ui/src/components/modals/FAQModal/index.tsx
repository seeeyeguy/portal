import React from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { faClose } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { FAQs } from "components/modals/FAQModal/props/faq"

import styles from "components/modals/FAQModal/styles/index.module.css";

export default function FAQModal() {
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

  const onClickClose = React.useCallback(
    (event: React.MouseEvent<HTMLElement>) => {
      const windowWidth = document.documentElement.clientWidth;
      const modalWidth = faqModalRef.current
        ? faqModalRef.current.clientWidth
        : 0;
      // Check if the mouse click was outside of the modal.
      if (faqModalRef.current && event.clientX < windowWidth - modalWidth) {
        navigate("/");
      }
    },
    [faqModalRef, navigate]
  );

  return (
    <dialog
      onClick={onClickClose}
      className={styles["faq-modal"]}
      ref={faqModalRef}
    >
      <header className={styles["faq-modal-header-row"]}>
        <h2>FAQ</h2>
        <button aria-description="faq modal close button" onClick={() => navigate("/")}>
          <FontAwesomeIcon icon={faClose} size="lg" />
        </button>
      </header>
      <div
        className={styles["faq-modal-content"]}
        aria-description="container for frequently asked questions"
      >
        {FAQs.map((faq, i) => (
          <details key={"faq" + i}>
            <summary>{faq.question}</summary>
            <p aria-description="faq answer">{faq.answer}</p>
          </details>
        ))}
      </div>
    </dialog>
  );
}
