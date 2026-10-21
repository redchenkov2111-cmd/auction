from fastapi import FastAPI 
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="NeoAuction Core Engine") 

auction_bids =[]
is_auction_active = True

app.mount("/static",StaticFiles(directory="static"),name="static")

class BidItem(BaseModel):
    price:int


@app.get("/", response_class = HTMLResponse) 
def serve_index():
    return FileResponse("index.html")

 
 
@app.post("/bid") 
def place_bid(item: BidItem): 
    global is_auction_active 
 
    if not is_auction_active: 
        return { 
            "status": "error", 
            "message": "Торги по данному лоту официально завершены!" 
        } 
 
    if not is_valid_bid(item.price): 
        return { 
            "status": "error", 
            "message": "Ставка не может быть ниже порога в 500 ₽" 
        } 
 
    auction_bids.append({"price": item.price}) 
 
    # Лимит лота: 10 ставок 
    if len(auction_bids) >= 10: 
        is_auction_active = False 
 
    return { 
        "status": "success", 
        "message": "Ставка принята", 
        "price": item.price, 
        "is_active": is_auction_active 
    }
@app.get("/bids")
def get_bids():
    recent_bids = auction_bids[::-1][:5]
    return {"bids": recent_bids}

@app.get("/analytics")
def get_analytics():
    bids_snapshot = list(auction_bids)
    highest_bid = max((b["price"] for b in bids_snapshot), default=0)

    return {
        "is_active": is_auction_active,
        "highest_bid": highest_bid,
        "platform_profit": calculate_platform_profit(bids_snapshot),
        "min_bid": 500,
        "bids_count": len(bids_snapshot),
    }


def is_valid_bid(price: int) -> bool: 
    return price >= 500

def calculate_platform_profit(bids_list: list) -> float: 
    total_volume = sum(bid["price"] for bid in bids_list) 
    profit = 0.0 
    if total_volume <= 10000: 
        profit = total_volume * 0.10 
    elif total_volume <= 50000: 
    # 10% с первых 10 000 + 7% с остатка 
        profit = (10000 * 0.10) + ((total_volume - 10000) * 0.07) 
    else: 
    # 10% с первых 10 000 + 7% со следующих 40 000 + 4% с остатка 
        profit = (10000 * 0.10) + (40000 * 0.07) + ((total_volume - 50000) * 0.04) 
    return round(profit, 2)

