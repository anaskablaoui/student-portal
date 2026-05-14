document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();

        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

        link.classList.add('active');
        document.getElementById(link.dataset.panel).classList.add('active');
    });
});


const sessionFilter = document.getElementById('absence-session')

sessionFilter.addEventListener("change",function (){
    const selected = this.value.trim();

    const rows = document.querySelectorAll("#absence-table tr")

    rows.forEach(row =>{
        const absence = row.dataset.seance.trim()

        if (selected ==="" || absence ==selected){
            row.style.display = ""
        }
        else{
            row.style.display = "none"
        }
    });
});

const groupeFilter = document.getElementById('note-groupe')

groupeFilter.addEventListener("change", function(){
    const selected = this.value.trim();

    const rows = document.querySelectorAll("#noteTable tr");

    rows.forEach(row=> {
        const groupe = row.dataset.groupe.trim()

        if(selected === "" || groupe == selected){
            row.style.display = ""
        }
        else{
            row.style.display = "none"
        }
    });
});