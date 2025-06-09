
document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll(".open-case-btn");
  const animationArea = document.getElementById("animation-area");
  const lid = document.querySelector(".lid");
  const itemFlyout = document.getElementById("item-flyout");
  const resultTable = document.getElementById("case-result");
  const resultBody = document.getElementById("case-result-body");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      const caseType = btn.getAttribute("data-case-type");

      // Reset UI
      lid.classList.remove("open");
      itemFlyout.classList.add("item-hidden");
      itemFlyout.textContent = "🎁";
      animationArea.style.display = "block";
      resultTable.style.display = "none";

      // Step 1: Animate lid
      setTimeout(() => {
        lid.classList.add("open");
      }, 200);

      // Step 2: Fetch instrument
      setTimeout(() => {
        fetch("/opening/open_case", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ case_type: caseType }),
        })
        .then(res => res.json())
        .then(data => {
          // Step 3: Show flying item
          itemFlyout.textContent = data.name;
          itemFlyout.classList.remove("item-hidden");

          // Step 4: Show result table
          setTimeout(() => {
            resultBody.innerHTML = `
              <tr>
                <td>${data.type}</td>
                <td>${data.name}</td>
                <td>${data.volume}</td>
                <td>${data.market_value}</td>
                <td>${data.open}</td>
                <td>${data.close}</td>
                <td>${data.profit}</td>
              </tr>
            `;
            resultTable.style.display = "block";
          }, 1500);
        });
      }, 1000);
    });
  });
});

