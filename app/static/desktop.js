document.addEventListener("DOMContentLoaded", function () {
    const instrumentInput = document.getElementById("instrumentSelector");
    const instrumentList = document.getElementById("instruments");

    const priceChartCtx = document.getElementById("priceChart").getContext("2d");
    const macdChartCtx = document.getElementById("macdChart").getContext("2d");
    const volumeChartCtx = document.getElementById("volumeChart").getContext("2d");

    let priceChart, macdChart, volumeChart;

    async function loadInstruments() {
        const res = await fetch("/desktop/api/instrument_list");
        const instruments = await res.json();

        instrumentList.innerHTML = "";
        instruments.forEach(inst => {
            const opt = document.createElement("option");
            opt.value = inst;
            instrumentList.appendChild(opt);
        });

        instrumentInput.value = instruments[0];
        loadChartData(instruments[0]);
    }

    async function loadChartData(instrument) {
        const res = await fetch(`/desktop/api/chart_data/${instrument}`);
        const data = await res.json();

        const { labels, price, macd, volume } = data;

        if (priceChart) priceChart.destroy();
        if (macdChart) macdChart.destroy();
        if (volumeChart) volumeChart.destroy();

        priceChart = new Chart(priceChartCtx, {
            type: "line",
            data: {
                labels,
                datasets: [{
                    label: "Price",
                    data: price,
                    borderColor: "blue",
                    fill: false
                }]
            }
        });

        macdChart = new Chart(macdChartCtx, {
            type: "bar",
            data: {
                labels,
                datasets: [
                    {
                        type: "line",
                        label: "MACD Line",
                        data: data.macd_line,
                        borderColor: "blue",
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        yAxisID: "y",
                    },
                    {
                        type: "line",
                        label: "Signal Line",
                        data: data.signal_line,
                        borderColor: "red",
                        backgroundColor: "transparent",
                        borderWidth: 2,
                        yAxisID: "y",
                    },
                    {
                        label: "Histogram",
                        data: data.histogram,
                        backgroundColor: ctx => {
                            const value = ctx.raw;
                            return value >= 0 ? "green" : "orange";
                        },
                        yAxisID: "y",
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: false
                    }
                },
                plugins: {
                    legend: {
                        position: "top",
                    },
                    title: {
                        display: true,
                        text: "MACD Indicator"
                    }
                }
            }
        });

        volumeChart = new Chart(volumeChartCtx, {
            type: "bar",
            data: {
                labels,
                datasets: [{
                    label: "Volume",
                    data: volume,
                    backgroundColor: "orange"
                }]
            }
        });
    }

    async function loadPortfolio() {
        const res = await fetch("/desktop/api/portfolio");
        const data = await res.json();

        const tableBody = document.querySelector("#positionsTable tbody");
        tableBody.innerHTML = "";

        data.positions.forEach(pos => {
            const profit = (pos.current_price - pos.open_price) * pos.volume * (pos.type === "Short" ? -1 : 1);
            const profitPct = (profit / (pos.open_price * pos.volume)) * 100;

            const row = `
                <tr>
                    <td>${pos.symbol}</td>
                    <td>${pos.type}</td>
                    <td>${pos.open_date}</td>
                    <td>${pos.open_price.toFixed(2)}</td>
                    <td>${pos.current_price.toFixed(2)}</td>
                    <td>${pos.volume}</td>
                    <td>${profit.toFixed(2)}</td>
                    <td>${profitPct.toFixed(2)}%</td>
                </tr>`;
            tableBody.innerHTML += row;
        });

        document.getElementById("invested").textContent = data.summary.invested.toFixed(2);
        document.getElementById("free-cash").textContent = data.summary.free_cash.toFixed(2);
        document.getElementById("total").textContent = data.summary.total.toFixed(2);
        document.getElementById("profit").textContent = data.summary.profit.toFixed(2);
        document.getElementById("profit-pct").textContent = data.summary.profit_pct.toFixed(2);
    }

    instrumentInput.addEventListener("change", () => {
        const value = instrumentInput.value;
        if (value) loadChartData(value);
    });

    loadInstruments();
    loadPortfolio();
});
