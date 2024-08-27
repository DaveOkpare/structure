from typing import Dict, Optional

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from utils import extract, scrape

app = FastAPI()


class Body(BaseModel):
    url: str
    prompt: str
    fields: Dict[str, str]
    xpath: Optional[str] = None


def process_website(url: str, prompt: str, xpath: str, fields: dict):
    context = scrape(url, xpath)
    output = extract(prompt, context, fields)
    print(output)


@app.post("/process")
def process_webpage(webpage: Body, bg_task: BackgroundTasks):
    bg_task.add_task(
        process_website, webpage.url, webpage.prompt, webpage.xpath, webpage.fields
    )
    return {"message": "Processing URL"}
