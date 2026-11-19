document.addEventListener("DOMContentLoaded", function () {
    const chart = document.getElementById("reviewChart");

    if (!chart) return;

    const genuine = Number(chart.dataset.genuine);
    const fake = Number(chart.dataset.fake);
    const total = genuine + fake;

    if (total === 0) {
        chart.textContent = "No reviews analyzed yet.";
        return;
    }

    const genuinePercent = (genuine / total) * 100;
    const fakePercent = (fake / total) * 100;

    chart.innerHTML = `
        <div style="
            width:180px;
            height:180px;
            border-radius:50%;
            background:conic-gradient(
                #38bdf8 0% ${genuinePercent}%,
                #f87171 ${genuinePercent}% 100%
            );
            margin:20px auto;
            display:grid;
            place-items:center;
        ">
            <div style="
                background:#151f35;
                border-radius:50%;
                width:125px;
                height:125px;
                display:grid;
                place-items:center;
                text-align:center;
                font-weight:bold;
                color:white;
            ">
                ${total} Reviews
            </div>
        </div>

        <p style="text-align:center">
            Genuine: ${genuinePercent.toFixed(1)}%
            |
            Flagged: ${fakePercent.toFixed(1)}%
        </p>
    `;
});
