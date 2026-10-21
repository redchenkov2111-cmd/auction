from fastapi import FastAPI 
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="NeoAuction Core Engine") 
app.mount("/static",StaticFiles(directory="static"),name="static")

class BidItem(BaseModel):
    price:int


@app.get("/", response_class = HTMLResponse) 
def serve_index():
    return FileResponse("index.html")

@app.post("/bid")
def place_bid(item:BidItem):
     return { 
        "status": "success", 
        "message": "Ставка принята", 
        "price": item.price} 