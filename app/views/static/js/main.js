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
});
