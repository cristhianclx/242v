from flask import Flask
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route("/data")
def data():
    r = requests.get("https://cuantoestaeldolar.pe/")
    raw = r.text
    soup = BeautifulSoup(raw, "html.parser")
    elements = soup.find_all("p", class_="ValueQuotation_text___mR_0")
    return {
        "sunat": {
            "compra": float(elements[2].text),
            "venta": float(elements[3].text)
        },
        "paralelo": {
            "compra": float(elements[0].text),
            "venta": float(elements[1].text)
        },
        "euro": {
            "compra": float(elements[6].text),
            "venta": float(elements[7].text)
        }
    }