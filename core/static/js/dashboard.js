document.addEventListener('DOMContentLoaded', function () {
    const dataEl = document.getElementById('dashboard-chart-data');
    const canvas = document.getElementById('dashboard-weight-chart');
    if (!dataEl || !canvas) {
        return;
    }

    const chartData = JSON.parse(dataEl.textContent);
    new Chart(canvas, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Weight (kg)',
                data: chartData.weights,
                borderColor: '#3a7d44',
                backgroundColor: '#3a7d44',
                tension: 0.2,
                pointRadius: 2,
            }],
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: false },
            },
        },
    });
});
