from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="webapp/templates")
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("base.html", {"request":request})


