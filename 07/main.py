from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api
import requests
from playwright.sync_api import Page, expect, sync_playwright


app = Flask(__name__)
api = Api(app)


class IndexResource(Resource):
    def get(self):
        return {}, 204


class PingResource(Resource):
    def get(self):
        return {
            "response": "PONG"
        }


class ExchangeResource(Resource):
    def get(self):
        exchanges = {}
        with sync_playwright() as playwright:
            ff = playwright.firefox
            browser = ff.launch(headless=True)
            page = browser.new_page()
            page.goto("https://e-consulta.sunat.gob.pe/cl-at-ittipcam/tcS01Alias")
            expect(page.locator("button.js-cal-option.btn.btn-default.active")).to_be_visible()
            html_raw = page.content()
            soup = BeautifulSoup(html_raw, 'html.parser')
            for x in soup.find_all("td", class_="calendar-day"):
                if "current" in x["class"]:
                     if len(x.find_all("div")) > 1:
                         exchanges[int(x.find_all("div")[0].text)] = {
                             "compra": float(x.find_all("div")[1].text.replace("Compra ", "")),
                             "venta": float(x.find_all("div")[2].text.replace("Venta ", "")),
                         }
            return exchanges


api.add_resource(IndexResource, "/")
api.add_resource(PingResource, "/ping")
api.add_resource(ExchangeResource, "/exchange")


if __name__ == "__main__":
    app.run(debug = True)
