document.addEventListener("DOMContentLoaded", function () {
    const ctxPrice = document.getElementById("priceChart").getContext("2d");
    const ctxMACD = document.getElementById("macdChart").getContext("2d");
    const ctxVolume = document.getElementById("volumeChart").getContext("2d");

    const priceChart = new Chart(ctxPrice, {
        type: "line",
        data: {
            labels: ["9:00", "10:00", "11:00", "12:00", "13:00"],
            datasets: [{
                label: "Price",
                data: [100, 102, 101.5, 103, 104],
                borderColor: "blue",
                fill: false
            }]
        },
    });

    const macdChart = new Chart(ctxMACD, {
        type: "line",
        data: {
            labels: ["9:00", "10:00", "11:00", "12:00", "13:00"],
            datasets: [{
                label: "MACD",
                data: [0.2, 0.1, -0.1, -0.05, 0.15],
                borderColor: "green",
                fill: false
            }]
        },
    });

    const volumeChart = new Chart(ctxVolume, {
        type: "bar",
        data: {
            labels: ["9:00", "10:00", "11:00", "12:00", "13:00"],
            datasets: [{
                label: "Volume",
                data: [1000, 2000, 1500, 3000, 2500],
                backgroundColor: "orange"
            }]
        }
    });

    function loadPortfolio() {
        fetch("/desktop/get_portfolio_data")
            .then(res => res.json())
            .then(data => {
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
            });
    }

    loadPortfolio();
});
