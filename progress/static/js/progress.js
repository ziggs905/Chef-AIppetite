document.addEventListener('DOMContentLoaded', function () {
    const dataEl = document.getElementById('chart-data');
    const canvas = document.getElementById('weight-chart');
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
            }],
        },
        options: {
            scales: {
                y: { beginAtZero: false },
            },
        },
    });
});
