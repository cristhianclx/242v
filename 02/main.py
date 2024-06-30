from flask import Flask
from bs4 import BeautifulSoup
import requests


app = Flask(__name__)


@app.route("/")
def index():
    return "hello world"


@app.route("/data")
def data():
    r = requests.get("https://cuantoestaeldolar.pe/", headers = {
        "Host": "cuantoestaeldolar.pe",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8,es-ES;q=0.5,es;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "DNT": "1",
        "Connection": "keep-alive",
    })
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