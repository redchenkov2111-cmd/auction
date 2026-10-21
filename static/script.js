const priceInput = document.getElementById("priceInput"); 
const buyBtn = document.getElementById("buyBtn"); 
const errorView = document.getElementById("errorView"); 
const bidsList = document.getElementById("bidsList"); 
 
function renderBids(bids) { 
    if (!bids || bids.length === 0) { 
        bidsList.innerHTML = '<li style="color: #64748b; border: none;">Ставок пока нет</li>'; 
        return; 
    } 
    bidsList.innerHTML = bids.map((b, idx) => ` 
        <li style="${idx === 0 ? 'border-left-color: #4ade80;' : 
''}"> 
            <span>${idx === 0 ? '🔥 Последняя ставка' : 'Предыдущая ставка'}</span> 
            <b>${b.price} ₽</b> 
        </li> 
    `).join(''); 
} 
 
function loadBids() { 
    fetch('/bids') 
        .then(res => res.json()) 
        .then(data => renderBids(data.bids)); 
} 
 
function sendBid() { 
    const val = parseInt(priceInput.value, 10); 
    if (isNaN(val)) { 
        errorView.className = "message error"; 
        errorView.innerText = "Пожалуйста, введите число"; 
        return; 
    } 
 
    fetch('/bid', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ price: val }) 
    }) 
    .then(response => response.json()) 
    .then(data => { 
        if (data.status === "error") { 
            errorView.className = "message error"; 
            errorView.innerText = data.message; 
        } else { 
            errorView.className = "message success"; 
            errorView.innerText = `${data.message}: 
${data.price} ₽`; 
            priceInput.value = ""; 
            loadBids();
            loadAnalytics();   // <-- добавить эту строку 
        }
        if (data.is_active === false) { lockAuctionUI(); }

}); 
} 

function lockAuctionUI() { 
    priceInput.disabled = true; 
    buyBtn.disabled = true; 
    buyBtn.innerText = "Торги закрыты"; 
    errorView.className = "message error"; 
    errorView.innerText = "Раунд завершен! Достигнут лимит ставок лота."; 
    }
function loadAnalytics() {
    fetch('/analytics')
        .then(res => res.json())
        .then(data => {
            document.getElementById("statusVal").innerText =
                data.is_active ? "Активны" : "Завершены";

            document.getElementById("highestVal").innerText =
                data.highest_bid ? `${data.highest_bid} ₽` : "—";

            document.getElementById("profitVal").innerText =
                `${data.platform_profit.toLocaleString('ru-RU')} ₽`;

            priceInput.placeholder = `Мин. ставка: ${data.min_bid} ₽`;
            priceInput.min = data.min_bid;

            if (!data.is_active) {
                lockAuctionUI();
            }
        });
}
    buyBtn.addEventListener("click", sendBid); 
    document.addEventListener("DOMContentLoaded", () => {
    loadBids();
    loadAnalytics();   // <-- добавить эту строку
});