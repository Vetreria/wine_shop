import datetime
import os
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import dotenv
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_goods(excel_path):
    goods = pandas.read_excel(excel_path, keep_default_na=False).to_dict(
        orient="records"
    )
    goods_group = defaultdict(list)
    for good in goods:
        goods_group[good["Категория"]].append(good)
    return goods_group


def get_years(start_year):
    year_now = datetime.datetime.now().year
    age = year_now - int(start_year)
    if age % 10 == 1 and age != 11 and age % 100 != 11:
        return "{0} год".format(age)
    elif 1 < age % 10 <= 4 and age != 12 and age != 13 and age != 14:
        return "{0} года".format(age)
    else:
        return "{0} лет".format(age)


def render_page(excel_path, start_year):
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    winery_age = "Уже {0} с вами".format(get_years(start_year))
    template = env.get_template("template.html")
    rendered_page = template.render(
        winery_age=winery_age, goods_group=get_goods(excel_path)
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def main():
    dotenv.load_dotenv()
    excel_path = os.getenv("EXCEL_PATH")
    start_year = os.getenv("START_YEAR")
    render_page(excel_path, start_year)
    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
