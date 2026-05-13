// Initialize navigation
function initNav() {
    const links = document.querySelectorAll(".nav-link");
    const panels = document.querySelectorAll(".panel");

    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const target = link.getAttribute("data-panel");
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");
            panels.forEach(panel => panel.classList.remove("active"));
            const activePanel = document.getElementById(target);
            if (activePanel) activePanel.classList.add("active");
        });
    });
}

