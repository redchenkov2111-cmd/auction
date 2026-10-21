from fastapi import FastAPI 
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="NeoAuction Core Engine") 
app.mount("/static",StaticFiles(directory="static"),name="static")
@app.get("/", response_class = HTMLResponse) 
def serve_index():
    return FileResponse("index.html")