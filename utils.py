import os
from typing import List
from dotenv import load_dotenv
import instructor
from lxml import html
from openai import OpenAI
from pydantic import BaseModel, create_model
import requests


load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = instructor.from_openai(OpenAI())


def scrape(url: str, xpath_exp: str = None):
    session = requests.Session()

    response = session.get(url)
    tree = html.fromstring(response.text)

    text = ""

    if xpath_exp:
        for article in tree.xpath(xpath_exp):
            text += article.text_content()
            text += "\n"
    else:
        text = tree.text_content()

    return text


def extract(sys_msg: str, context: str, fields: list):
    attributes = {key: (str, ...) for key in fields}

    datamodel = create_model("DataModel", **attributes)

    class MultiOutput(BaseModel):
        data: List[datamodel]  # type: ignore

    extracted_data = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=MultiOutput,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": context},
        ],
    )

    output = extracted_data.model_dump_json(indent=2)
    return output


def process_website(url: str, prompt: str, fields: list, xpath: str = None):
    context = scrape(url, xpath)
    output = extract(prompt, context, fields)
    return output
