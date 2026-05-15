document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();

        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

        link.classList.add('active');
        document.getElementById(link.dataset.panel).classList.add('active');
    });
});

const matiereFilter = document.getElementById("matiereFilter");
const matiereFilterAbsence = document.getElementById("matiereFilter2");

matiereFilterAbsence.addEventListener("change",function () {
    const selected = this.value.trim();

    const rows = document.querySelectorAll("#absenceTable tr")

    rows.forEach(row => {
        const absence = row.dataset.matiere.trim();

        if (selected === "" || absence == selected) {
            row.style.display = "";
        }
        else{
            row.style.display = "none";
        }
    });
});

matiereFilter.addEventListener("change", function () {

    const selected = this.value.trim();

    const rows = document.querySelectorAll("#notesTable tr");

 

    rows.forEach(row => {

        const matiere = row.dataset.matiere.trim();

        if (selected === "" || matiere == selected) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }

    });

    
});

console.log("hhhhh")


function ouvrirStats() {
    const modal = document.getElementById('statsModal');
    modal.style.display = 'flex';

    // Charge les données et crée le graphique
    fetch('{% url "etudiant_stats" %}')
        .then(res => res.json())
        .then(data => {
            const ctx = document.getElementById('notesChart').getContext('2d');

            // Détruit le graphique existant si déjà créé
            if (window.notesChartInstance) {
                window.notesChartInstance.destroy();
            }

            window.notesChartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Mes notes /20',
                        data: data.notes,
                        backgroundColor: data.notes.map(note =>
                            note >= 10 ? 'rgba(91,126,229,0.8)' : 'rgba(229,57,53,0.7)'
                        ),
                        borderColor: data.notes.map(note =>
                            note >= 10 ? '#5b7ee5' : '#e53935'
                        ),
                        borderWidth: 2,
                        borderRadius: 8,
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: ctx => `Note : ${ctx.raw}/20`
                            }
                        }
                    },
                    scales: {
                        y: { min: 0, max: 20, ticks: { stepSize: 2 } },
                        x: { grid: { display: false } }
                    }
                }
            });
        });
}

function fermerStats() {
    document.getElementById('statsModal').style.display = 'none';
}

// Fermer en cliquant sur le fond
document.getElementById('statsModal').addEventListener('click', function(e) {
    if (e.target === this) fermerStats();
});