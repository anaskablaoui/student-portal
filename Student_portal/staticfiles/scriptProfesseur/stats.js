const labels = JSON.parse(document.getElementById('labels-data').textContent);
const data   = JSON.parse(document.getElementById('data-values').textContent);

const ctx = document.getElementById('absenceChart');  // ← corrigé

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: labels,
        datasets: [{
            label: 'Mes notes',
            data: data,
            backgroundColor: 'rgba(116, 148, 236, 0.6)',
            borderColor: '#5b7ee5',
            borderWidth: 2,
            borderRadius: 8,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true,
                max: 20
            }
        }
    }
});