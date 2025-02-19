import React from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { faClose, faStar } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import styles from "components/modals/IntroModal/styles/index.module.css";

const VISITED_KEY = "hasVisited";

export default function IntroModal() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const [showModal, setShowModal] = React.useState(
    localStorage.getItem(VISITED_KEY) === null && !searchParams?.get("faq")
  );

  const handleClickOutside = (
    event: React.MouseEvent<HTMLDialogElement, MouseEvent>
  ) => {
    if (event.target === event.currentTarget) {
      handleClose();
    }
  };

  const handleClose = React.useCallback(() => {
    setShowModal(false);
    localStorage.setItem(VISITED_KEY, "true");
  }, [setShowModal]);

  return (
    <dialog
      open={showModal}
      className={styles["intro-modal"]}
      onClick={handleClickOutside}
    >
      <section className={styles["modal-content"]}>
        <button
          className={styles["close"]}
          onClick={handleClose}
          aria-label="close"
        >
          <FontAwesomeIcon icon={faClose} />
        </button>
        <header className={styles["modal-header"]}>
          <h2>Welcome to The Portal!</h2>
        </header>
        <main className={styles["modal-body"]}>
          <h3>Since it is your first time visiting us, here are some tips:</h3>
          <ul>
            <li>
              When you filter using the Role and Function buttons, we save your
              selections. Next time you visit, they’ll reload.
            </li>
            <li>
              Hover and click the{" "}
              <FontAwesomeIcon icon={faStar} data-testid="faStar-icon" /> to add
              or remove a resource from your favorites.
            </li>
            <li>
              The Portal provides links to content, however, those resources
              control access using their own processes – please consider whether
              you need access to a resource prior to submitting a request.
            </li>
          </ul>
        </main>
        <footer className={styles["modal-footer"]}>
          <h3>Any Questions?</h3>
          <a
            onClick={() => {
              handleClose();
              navigate("/?faq=true");
            }}
          >
            Visit our FAQ
          </a>
        </footer>
      </section>
    </dialog>
  );
}
