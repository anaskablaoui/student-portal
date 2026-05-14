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