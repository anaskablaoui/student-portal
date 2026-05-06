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

// Fetch and render calendar
function loadCalendar() {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    const today = new Date();
    const year = today.getFullYear();
    const month = today.getMonth();

    fetch('/professeur/sessions-json/')
        .then(response => response.json())
        .then(sessions => renderCalendar(year, month, sessions, calendarEl))
        .catch(error => {
            console.error('Error loading sessions:', error);
            renderCalendar(year, month, [], calendarEl);
        });
}

// Render calendar grid
function renderCalendar(year, month, sessions, calendarEl) {
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const startDayOfWeek = (firstDay.getDay() - 1 + 7) % 7;
    
    let html = '<div class="cal-grid">';
    const daysOfWeek = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];
    
    daysOfWeek.forEach(day => {
        html += `<div class="cal-day-label">${day}</div>`;
    });

    for (let i = 0; i < startDayOfWeek; i++) {
        html += '<div class="cal-day empty"></div>';
    }

    for (let day = 1; day <= lastDay.getDate(); day++) {
        const currentDate = new Date(year, month, day);
        const isToday = currentDate.toDateString() === new Date().toDateString();
        const dayEvents = sessions.filter(session => {
            const sessionDate = new Date(session.start);
            return sessionDate.getDate() === day && 
                   sessionDate.getMonth() === month && 
                   sessionDate.getFullYear() === year;
        });

        html += `<div class="cal-day ${isToday ? 'today' : ''}">
            <div>${day}</div>
            ${dayEvents.length > 0 ? '<div class="cal-events">' + dayEvents.map(e => `<div class="cal-event" title="${e.title}">•</div>`).join('') + '</div>' : ''}
        </div>`;
    }

    const totalCells = startDayOfWeek + lastDay.getDate();
    const remainingCells = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
    for (let i = 0; i < remainingCells; i++) {
        html += '<div class="cal-day empty"></div>';
    }

    html += '</div>';
    calendarEl.innerHTML = html;
}

// Run when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initNav();
        loadCalendar();
    });
} else {
    initNav();
    loadCalendar();
}
