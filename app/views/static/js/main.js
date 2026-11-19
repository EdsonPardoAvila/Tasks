document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.querySelector(".menu-toggle");
    const overlay = document.querySelector(".overlay");

    if (toggle) {
        toggle.addEventListener("click", function () {
            document.body.classList.toggle("sidebar-open");
        });
    }

    if (overlay) {
        overlay.addEventListener("click", function () {
            document.body.classList.remove("sidebar-open");
        });
    }

    const path = window.location.pathname;
    document.querySelectorAll(".sidebar a").forEach(function (link) {
        const href = link.getAttribute("href");
        if (href === path || (href !== "/" && path.startsWith(href))) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });

    const confirmModal = document.getElementById("confirm-modal");
    const confirmMessage = document.getElementById("confirm-message");
    const confirmAccept = document.getElementById("confirm-accept");
    let pendingForm = null;

    const closeConfirm = function () {
        confirmModal.hidden = true;
        pendingForm = null;
    };

    document.querySelectorAll("form[data-confirm]").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (form.dataset.confirmed === "1") {
                return;
            }
            event.preventDefault();
            pendingForm = form;
            confirmMessage.textContent = form.getAttribute("data-confirm");
            confirmModal.hidden = false;
            confirmAccept.focus();
        });
    });

    if (confirmModal) {
        document.querySelectorAll("[data-confirm-close]").forEach(function (el) {
            el.addEventListener("click", closeConfirm);
        });

        confirmModal.addEventListener("click", function (event) {
            if (event.target === confirmModal) {
                closeConfirm();
            }
        });

        confirmAccept.addEventListener("click", function () {
            const form = pendingForm;
            closeConfirm();
            if (form) {
                form.dataset.confirmed = "1";
                form.submit();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && !confirmModal.hidden) {
                closeConfirm();
            }
        });
    }

    const flashEl = document.getElementById("flash-messages");
    if (flashEl && typeof Notyf !== "undefined") {
        const notyf = new Notyf({
            duration: 3000,
            position: { x: "right", y: "top" },
            ripple: true,
        });

        let messages = [];
        try {
            messages = JSON.parse(flashEl.textContent);
        } catch (e) {
            messages = [];
        }

        messages.forEach(function (item) {
            const category = item[0];
            const message = item[1];
            if (category === "error") {
                notyf.error(message);
            } else {
                notyf.success(message);
            }
        });
    }

    const modal = document.getElementById("user-modal");
    const form = document.getElementById("user-form");
    const modalTitle = document.getElementById("modal-title");
    const modalSubmit = document.getElementById("modal-submit");
    const btnNew = document.getElementById("btn-new-user");

    if (modal && form) {
        const openModal = function () {
            modal.hidden = false;
            document.getElementById("username").focus();
        };

        const closeModal = function () {
            modal.hidden = true;
            form.reset();
            form.action = "";
        };

        if (btnNew) {
            btnNew.addEventListener("click", function () {
                modalTitle.textContent = "Nuevo usuario";
                modalSubmit.textContent = "Crear usuario";
                form.action = modal.getAttribute("data-create-url");
                openModal();
            });
        }

        document.querySelectorAll(".btn-edit").forEach(function (btn) {
            btn.addEventListener("click", function () {
                modalTitle.textContent = "Editar usuario";
                modalSubmit.textContent = "Guardar cambios";
                form.action = "/users/" + btn.getAttribute("data-id");
                document.getElementById("username").value = btn.getAttribute("data-username");
                document.getElementById("email").value = btn.getAttribute("data-email");
                openModal();
            });
        });

        document.querySelectorAll("[data-modal-close]").forEach(function (el) {
            el.addEventListener("click", closeModal);
        });

        modal.addEventListener("click", function (event) {
            if (event.target === modal) {
                closeModal();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && !modal.hidden) {
                closeModal();
            }
        });
    }
});
