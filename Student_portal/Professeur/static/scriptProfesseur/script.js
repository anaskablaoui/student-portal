document.addEventListener("DOMContentLoaded", () => {
    const links = document.querySelectorAll(".nav-link");
    const panels = document.querySelectorAll(".panel");

    links.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();

            const target = link.getAttribute("data-panel");

            // remove active from all links
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            // hide all panels
            panels.forEach(panel => panel.classList.remove("active"));

            // show selected panel
            const activePanel = document.getElementById(target);
            if (activePanel) {
                activePanel.classList.add("active");
            }
        });
    });
});
//full calendar code
document.addEventListener('DOMContentLoaded', function () {

    const calendarEl = document.getElementById('calendar');

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/professeur/sessions-json/', // make sure URL is correct
    });

    calendar.render();

    // 🔥 VERY IMPORTANT FIX
    setTimeout(() => {
        calendar.updateSize();
    }, 500);
});