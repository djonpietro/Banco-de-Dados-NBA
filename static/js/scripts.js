document.addEventListener("DOMContentLoaded", function () {
    const exportButton = document.getElementById("exportButton");
    if (exportButton) {
        exportButton.addEventListener("click", function () {
            let table = document.querySelector("table");
            if (table) {
                let csv = [];
                let rows = table.querySelectorAll("tr");

                for (let i = 0; i < rows.length; i++) {
                    let row = [], cols = rows[i].querySelectorAll("td, th");
                    for (let j = 0; j < cols.length; j++) {
                        row.push(cols[j].innerText);
                    }
                    csv.push(row.join(","));
                }

                let csvFile = new Blob([csv.join("\n")], { type: "text/csv" });
                let downloadLink = document.createElement("a");
                downloadLink.download = "table.csv";
                downloadLink.href = window.URL.createObjectURL(csvFile);
                downloadLink.style.display = "none";
                document.body.appendChild(downloadLink);
                downloadLink.click();
                document.body.removeChild(downloadLink);
            }
        });
    }
});
