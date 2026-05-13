document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();

        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));

        link.classList.add('active');
        document.getElementById(link.dataset.panel).classList.add('active');
    });
});


