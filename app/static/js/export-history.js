document.addEventListener("DOMContentLoaded", () => {
    const button = document.getElementById("exportHistoryCsv");
    const table = document.querySelector("#reviewHistory table");

    if (!button || !table) {
        console.warn("CSV export elements not found.");
        return;
    }

    button.addEventListener("click", () => {
        const rows = [...table.querySelectorAll("tbody tr")]
            .filter(row =>
                row.cells.length >= 3 &&
                !row.hidden &&
                getComputedStyle(row).display !== "none"
            );

        if (!rows.length) {
            alert("No visible reviews to export.");
            return;
        }

        const escapeCSV = value =>
            '"' + value.replace(/"/g, '""') + '"';

        const data = [
            ["Review", "Prediction", "Score"],
            ...rows.map(row => [
                row.cells[0].textContent.trim(),
                row.cells[1].textContent.trim(),
                row.cells[2].textContent.trim()
            ])
        ];

        const csv = data
            .map(row => row.map(escapeCSV).join(","))
            .join("\r\n");

        const blob = new Blob(["\uFEFF", csv], {
            type: "text/csv;charset=utf-8;"
        });

        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = "CyberPulse_Review_History.csv";

        document.body.appendChild(link);
        link.click();
        link.remove();

        setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
});
