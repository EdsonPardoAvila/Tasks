document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");
    if (!calendarEl || typeof FullCalendar === "undefined") {
        return;
    }

    var dropdown = document.getElementById("event-dropdown");
    var detailModal = document.getElementById("event-detail-modal");
    var detailName = document.getElementById("detail-name");
    var detailPeriod = document.getElementById("detail-period");
    var detailDescription = document.getElementById("detail-description");
    var deleteForm = document.getElementById("event-delete-form");
    var selectedEvent = null;
    var dropdownOpenedAt = 0;

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: "dayGridMonth",
        locale: "es",
        headerToolbar: {
            left: "prev,next today",
            center: "title",
            right: "dayGridMonth,dayGridWeek,dayGridDay",
        },
        buttonText: {
            today: "Hoy",
            month: "Mes",
            week: "Semana",
            day: "Día",
        },
        events: calendarEl.dataset.eventsUrl || "/calendar/api/events",
        height: "auto",
        firstDay: 1,
        dayMaxEvents: 3,
        dateClick: function (info) {
            closeDropdown();
            openCreateModal(info.date);
        },
        eventClick: function (info) {
            info.jsEvent.preventDefault();
            info.jsEvent.stopPropagation();
            if (info.event.extendedProps && info.event.extendedProps.holiday) {
                closeDropdown();
                openDetailModal(info.event);
                return;
            }
            selectedEvent = info.event;
            openDropdown(info.jsEvent);
        },
    });
    calendar.render();

    var modal = document.getElementById("event-modal");
    var form = document.getElementById("event-form");
    var modalTitle = document.getElementById("event-modal-title");
    var modalSubmit = document.getElementById("event-modal-submit");
    var btnNew = document.getElementById("btn-new-event");
    var inputTitle = document.getElementById("event-title");
    var inputDescription = document.getElementById("event-description");
    var inputAllDay = document.getElementById("event-all-day");
    var inputStart = document.getElementById("event-start");
    var inputEnd = document.getElementById("event-end");

    if (!modal || !form) {
        return;
    }

    function pad(n) {
        return (n < 10 ? "0" : "") + n;
    }

    function toLocalInput(date) {
        if (!date) {
            return "";
        }
        var d = new Date(date);
        return (
            d.getFullYear() +
            "-" +
            pad(d.getMonth() + 1) +
            "-" +
            pad(d.getDate()) +
            "T" +
            pad(d.getHours()) +
            ":" +
            pad(d.getMinutes())
        );
    }

    function resetColor(color) {
        var radios = form.querySelectorAll('input[name="color"]');
        radios.forEach(function (radio) {
            radio.checked = radio.value === (color || "#dbeafe");
        });
    }

    function openModal() {
        modal.hidden = false;
        inputTitle.focus();
    }

    function closeModal() {
        modal.hidden = true;
        form.reset();
        form.action = "";
        resetColor("#dbeafe");
        inputAllDay.checked = false;
    }

    function openCreateModal(date) {
        modalTitle.textContent = "Nuevo evento";
        modalSubmit.textContent = "Crear evento";
        form.action = modal.getAttribute("data-create-url");

        var start = date ? new Date(date) : new Date();
        start.setHours(9, 0, 0, 0);
        var end = new Date(start);
        end.setHours(start.getHours() + 1);

        inputTitle.value = "";
        inputDescription.value = "";
        inputAllDay.checked = false;
        inputStart.type = "datetime-local";
        inputEnd.type = "datetime-local";
        inputStart.value = toLocalInput(start);
        inputEnd.value = toLocalInput(end);
        resetColor("#dbeafe");
        openModal();
    }

    function openEditModal(event) {
        modalTitle.textContent = "Editar evento";
        modalSubmit.textContent = "Guardar cambios";
        form.action = "/calendar/events/" + event.id;

        inputTitle.value = event.title || "";
        inputDescription.value = event.extendedProps.description || "";
        inputAllDay.checked = !!event.allDay;

        var start = event.start;
        var end = event.end;
        if (event.allDay) {
            inputStart.type = "date";
            inputEnd.type = "date";
            if (start) {
                var s = new Date(start);
                inputStart.value =
                    s.getFullYear() + "-" + pad(s.getMonth() + 1) + "-" + pad(s.getDate());
            } else {
                inputStart.value = "";
            }
            if (end) {
                var e = new Date(end);
                e.setDate(e.getDate() - 1);
                inputEnd.value =
                    e.getFullYear() + "-" + pad(e.getMonth() + 1) + "-" + pad(e.getDate());
            } else {
                inputEnd.value = "";
            }
        } else {
            inputStart.type = "datetime-local";
            inputEnd.type = "datetime-local";
            inputStart.value = toLocalInput(start);
            inputEnd.value = toLocalInput(end);
        }

        resetColor(event.backgroundColor || event.color || "#dbeafe");
        openModal();
    }

    var dateFormat = new Intl.DateTimeFormat("es", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
    });
    var dateTimeFormat = new Intl.DateTimeFormat("es", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    });

    function formatPeriod(event) {
        if (!event.start) {
            return "";
        }
        if (event.allDay) {
            var day = dateFormat.format(event.start);
            day = day.charAt(0).toUpperCase() + day.slice(1);
            if (event.end) {
                var last = new Date(event.end);
                last.setDate(last.getDate() - 1);
                var lastStr = dateFormat.format(last);
                if (last.toDateString() !== event.start.toDateString()) {
                    return day + " — " + lastStr;
                }
            }
            return day;
        }
        var startStr = dateTimeFormat.format(event.start);
        startStr = startStr.charAt(0).toUpperCase() + startStr.slice(1);
        if (event.end) {
            return startStr + " — " + dateTimeFormat.format(event.end);
        }
        return startStr;
    }

    function openDetailModal(event) {
        detailName.textContent = event.title || "Sin título";
        detailPeriod.textContent = formatPeriod(event);
        var desc = "";
        if (event.extendedProps) {
            desc = (event.extendedProps.description || "").trim();
        }
        detailDescription.textContent = desc || "Sin descripción";
        detailModal.hidden = false;
    }

    function closeDetailModal() {
        detailModal.hidden = true;
    }

    function openDropdown(jsEvent) {
        if (!dropdown) {
            return;
        }
        dropdown.hidden = false;
        dropdownOpenedAt = Date.now();
        var rect = dropdown.getBoundingClientRect();
        var x = jsEvent.clientX;
        var y = jsEvent.clientY;
        var left = Math.min(x, window.innerWidth - rect.width - 8);
        var top = y;
        if (top + rect.height > window.innerHeight - 8) {
            top = Math.max(8, y - rect.height);
        }
        dropdown.style.left = Math.max(8, left) + "px";
        dropdown.style.top = top + "px";
    }

    function closeDropdown() {
        if (dropdown) {
            dropdown.hidden = true;
        }
        selectedEvent = null;
    }

    if (dropdown) {
        dropdown.querySelectorAll("[data-action]").forEach(function (btn) {
            btn.addEventListener("click", function () {
                var action = btn.getAttribute("data-action");
                var event = selectedEvent;
                closeDropdown();
                if (!event) {
                    return;
                }
                if (action === "view") {
                    openDetailModal(event);
                } else if (action === "edit") {
                    openEditModal(event);
                } else if (action === "delete") {
                    if (deleteForm) {
                        deleteForm.action = "/calendar/events/" + event.id + "/delete";
                        deleteForm.dataset.confirmed = "";
                        deleteForm.dispatchEvent(
                            new Event("submit", { bubbles: true, cancelable: true })
                        );
                    }
                }
            });
        });

        document.addEventListener("click", function (event) {
            if (dropdown.hidden) {
                return;
            }
            if (Date.now() - dropdownOpenedAt < 150) {
                return;
            }
            if (event.target.closest && event.target.closest(".fc-event")) {
                return;
            }
            if (!dropdown.contains(event.target)) {
                closeDropdown();
            }
        });

        document.addEventListener("keydown", function (event) {
            if (event.key === "Escape" && !dropdown.hidden) {
                closeDropdown();
            }
        });

        window.addEventListener("scroll", closeDropdown, true);
    }

    document.querySelectorAll("[data-detail-close]").forEach(function (el) {
        el.addEventListener("click", closeDetailModal);
    });

    if (detailModal) {
        detailModal.addEventListener("click", function (event) {
            if (event.target === detailModal) {
                closeDetailModal();
            }
        });
    }

    if (btnNew) {
        btnNew.addEventListener("click", function () {
            closeDropdown();
            openCreateModal(null);
        });
    }

    document.querySelectorAll("[data-event-modal-close]").forEach(function (el) {
        el.addEventListener("click", closeModal);
    });

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            if (!modal.hidden) {
                closeModal();
            } else if (detailModal && !detailModal.hidden) {
                closeDetailModal();
            }
        }
    });

    inputAllDay.addEventListener("change", function () {
        if (inputAllDay.checked) {
            if (inputStart.value) {
                inputStart.type = "date";
                inputStart.value = inputStart.value.slice(0, 10);
            } else {
                inputStart.type = "date";
            }
            if (inputEnd.value) {
                inputEnd.type = "date";
                inputEnd.value = inputEnd.value.slice(0, 10);
            } else {
                inputEnd.type = "date";
            }
        } else {
            inputStart.type = "datetime-local";
            inputEnd.type = "datetime-local";
            if (inputStart.value && inputStart.value.length === 10) {
                inputStart.value = inputStart.value + "T09:00";
            }
            if (inputEnd.value && inputEnd.value.length === 10) {
                inputEnd.value = inputEnd.value + "T10:00";
            }
        }
    });
});
