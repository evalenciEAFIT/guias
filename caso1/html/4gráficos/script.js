document.addEventListener('DOMContentLoaded', function() {
    // Datos comunes para los gráficos
    const labels = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'];
    const datos = [12, 19, 3, 5, 2];
    const coloresFondo = [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)'
    ];
    const coloresBorde = [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)'
    ];

    // Gráfico de Barras
    const ctxBarras = document.getElementById('graficoBarras').getContext('2d');
    new Chart(ctxBarras, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ventas Mensuales',
                data: datos,
                backgroundColor: coloresFondo,
                borderColor: coloresBorde,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                title: { display: true, text: 'Gráfico de Barras' }
            }
        }
    });

    // Gráfico de Líneas
    const ctxLineas = document.getElementById('graficoLineas').getContext('2d');
    new Chart(ctxLineas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ventas Mensuales',
                data: datos,
                backgroundColor: coloresFondo[1],
                borderColor: coloresBorde[1],
                borderWidth: 2,
                fill: false
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            },
            plugins: {
                title: { display: true, text: 'Gráfico de Líneas' }
            }
        }
    });

    // Gráfico de Pastel
    const ctxPastel = document.getElementById('graficoPastel').getContext('2d');
    new Chart(ctxPastel, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ventas Mensuales',
                data: datos,
                backgroundColor: coloresFondo,
                borderColor: coloresBorde,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: { display: true, text: 'Gráfico de Pastel' }
            }
        }
    });

    // Gráfico de Área Polar
    const ctxPolar = document.getElementById('graficoPolar').getContext('2d');
    new Chart(ctxPolar, {
        type: 'polarArea',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ventas Mensuales',
                data: datos,
                backgroundColor: coloresFondo,
                borderColor: coloresBorde,
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                title: { display: true, text: 'Gráfico de Área Polar' }
            }
        }
    });
});