from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from transformers import pipeline

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Load Hugging Face text generation pipeline
generator = pipeline("text-generation", model="distilgpt2")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate", response_class=HTMLResponse)
async def generate_text(request: Request, prompt: str = Form(...)):
    result = generator(prompt, max_length=50, num_return_sequences=1)
    output = result[0]['generated_text']
    return templates.TemplateResponse("index.html", {
        "request": request, "prompt": prompt, "output": output
    })
