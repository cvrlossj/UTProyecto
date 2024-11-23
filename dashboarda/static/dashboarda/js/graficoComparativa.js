document.addEventListener("DOMContentLoaded", function () {
    const ctx = document.getElementById('juntasChart').getContext('2d');

    fetch('/superadmin/dashboard/juntas_chart_data/')
        .then(response => response.json())
        .then(data => {
            const { labels, integradas, inhabilitadas } = data;

            new Chart(ctx, {
                type: 'bar', 
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Integradas',
                            data: integradas,
                            backgroundColor: 'rgba(75, 192, 192, 0.6)',
                            borderColor: 'rgba(75, 192, 192, 1)',
                            borderWidth: 2
                        },
                        {
                            label: 'Inhabilitadas',
                            data: inhabilitadas,
                            backgroundColor: 'rgba(255, 99, 132, 0.6)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 2
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'top'
                        },
                        tooltip: {
                            mode: 'index',
                            intersect: false
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Fecha'
                            },
                            grid: {
                                display: false
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Cantidad'
                            },
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1,
                                precision: 0
                            }
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching chart data:', error));
});