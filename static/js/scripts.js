document.addEventListener("DOMContentLoaded", function () {
    const exportButton = document.getElementById("exportButton");
    if (exportButton) {
        exportButton.addEventListener("click", function () {
            let table = document.querySelector("table");
            let csv = [];
            let rows = table.querySelectorAll("tr");

            for (let row of rows) {
                let cols = row.querySelectorAll("td, th");
                let rowCsv = [];
                for (let col of cols) {
                    rowCsv.push(col.innerText);
                }
                csv.push(rowCsv.join(","));
            }

            let csvFile = new Blob([csv.join("\n")], { type: "text/csv" });
            let downloadLink = document.createElement("a");
            downloadLink.download = "table.csv";
            downloadLink.href = window.URL.createObjectURL(csvFile);
            downloadLink.style.display = "none";
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
        });
    }

    if (results && queryNumber) {
        let labels = [], data = [], labelX = '', labelY = 'Resultados';
        let chartType = 'bar';
        let chartOptions = {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: ''
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: labelY
                    }
                }
            }
        };

        switch (queryNumber) {
            case 1:
                labels = results.map(row => row[0]);
                data = results.map(row => row[1]);
                labelX = 'Cidade';
                break;
            case 2:
                labels = results.map(row => `${row[0]}; ${row[2]}`);
                data = results.map(row => row[3]);
                labelX = 'Jogador';
                labelY = 'Nº de Temporadas'
                break;
            case 3:
                labels = results.map(row => `${row[1]} x ${row[2]}`);
                data = results.map(row => row[5]);
                labelX = 'Jogo';
                labelY = 'Diferença de Pontos'
                break;
            case 4:
                labels = results.map(row => `${row[0]} ${row[1]}`);
                data = results.map(row => row[2]);
                labelX = 'Time';
                labelY = 'Nº de vitórias em casa'
                break;
            case 5:
                labels = results.map(row => `${row[2]}: ${row[0]} ${row[1]}`);
                data = results.map(row => row[3]);
                labelX = 'Temporada';
                labelY = 'Nº de vitórias na temporada'
                break;
            case 6:
                labels = results.map(row => row[0]);
                data = results.map(row => row[2]);
                labelX = 'Jogador';
                labelY = 'Numero de Times'
                break;
            default:
                break;
        }

        chartOptions.scales.x.title.text = labelX;

        let ctx = document.getElementById(`chart${queryNumber}`).getContext('2d');
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: labels,
                datasets: [{
                    label: labelY,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: chartOptions
        });
    }
});
