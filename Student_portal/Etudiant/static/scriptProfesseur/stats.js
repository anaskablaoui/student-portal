const labels = JSON.parse(document.getElementById('labels-data').textContent);
const data = JSON.parse(document.getElementById('data-values').textContent);

const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'bar', // or 'pie', 'line'
    data: {
        labels: labels,
        datasets: [{
            label: 'Mes notes',
            data: data,
            borderWidth: 1
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