
document.addEventListener("DOMContentLoaded", function () {
    const instrumentInput = document.getElementById("instrument");
    const volumeInput = document.getElementById("volume");
    const priceField = document.getElementById("price");
    const typeField = document.getElementById("instrument-type");
    const finalPriceField = document.getElementById("final-price");
    const stopLoss = document.getElementById("stopLoss");
    const sellButton = document.getElementById("sell-button");
    const buyButton = document.getElementById("buy-button");

    let currentInstrument = null;

    instrumentInput.addEventListener("input", () => {
        const symbol = instrumentInput.value.trim().toUpperCase();
        if (!symbol) return;

        fetch("/order/get_instrument_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ symbol })
        })
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    typeField.value = "--";
                    priceField.value = "--";
                    finalPriceField.value = "--";
                    sellButton.disabled = true;
                } else {
                    currentInstrument = data;
                    typeField.value = data.type;
                    priceField.value = data.price.toFixed(2);
                    sellButton.disabled = data.holdings <= 0;
                    updateFinalPrice();
                }
            });
    });

    volumeInput.addEventListener("input", updateFinalPrice);

    function updateFinalPrice() {
        const volume = parseFloat(volumeInput.value);
        if (!currentInstrument || isNaN(volume)) {
            finalPriceField.value = "--";
            return;
        }
        const total = volume * currentInstrument.price;
        finalPriceField.value = total.toFixed(2) + " USD";
    }

    document.getElementById("order-form").addEventListener("submit", function (e) {
        e.preventDefault();
        const volume = parseFloat(volumeInput.value);
        const symbol = instrumentInput.value.trim().toUpperCase();

        fetch("/order/submit_order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                action: "buy",
                symbol: symbol,
                volume: volume,
                stopLoss: stopLoss.value || null
            })
        })
            .then(res => res.json())
            .then(data => {
                alert(data.message || "Order sent");
            });
    });

    sellButton.addEventListener("click", function () {
        const volume = parseFloat(volumeInput.value);
        const symbol = instrumentInput.value.trim().toUpperCase();

        fetch("/order/submit_order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                action: "sell",
                symbol: symbol,
                volume: volume,
                stopLoss: stopLoss.value || null
            })
        })
            .then(res => res.json())
            .then(data => {
                alert(data.message || "Sell order sent");
            });
    });
});