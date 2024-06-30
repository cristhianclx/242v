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
    compra = float(elements[2].text)
    venta = float(elements[3].text)
    return {
        "sunat": {
            "compra": compra,
            "venta": venta
        },
        "paralelo": {}, # revisar elements
        "euro": {} # revisar elements
    }