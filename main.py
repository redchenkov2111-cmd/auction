from fastapi import FastAPI 
from fastapi.responses import HTMLResponse 
app = FastAPI(title="NeoAuction Core Engine") 
@app.get("/", response_class=HTMLResponse) 
def serve_index(): 
    with open("index.html", "r", encoding="utf-8") as file: 
        return file.read()