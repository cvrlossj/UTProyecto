document.addEventListener("DOMContentLoaded", function () {
 const ctx = document.getElementById('chartCanvas').getContext('2d');

 // Llamada al endpoint vecinos_chart_data
 fetch('/juntavecinos/dashboard/vecinos_chart_data/')
     .then(response => response.json())
     .then(data => {
         const { labels, integrados, inhabilitados } = data;

         new Chart(ctx, {
             type: 'bar',
             data: {
                 labels: labels, 
                 datasets: [
                     {
                         label: 'Integrados',
                         data: integrados, // Datos de vecinos integrados
                         backgroundColor: 'rgba(54, 162, 235, 0.6)',
                         borderColor: 'rgba(54, 162, 235, 1)',
                         fill: true,
                         tension: 0.4, // Para suavizar líneas
                         borderWidth: 2
                     },
                     {
                         label: 'Inhabilitados',
                         data: inhabilitados, // Datos de vecinos inhabilitados
                         backgroundColor: 'rgba(255, 99, 132, 0.6)',
                         borderColor: 'rgba(255, 99, 132, 1)',
                         fill: true,
                         tension: 0.4,
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
                             text: 'Cantidad de Vecinos'
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