import datetime
import os
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import dotenv
import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_data(data_goods):
    goods_list = pandas.read_excel(data_goods, keep_default_na=False).to_dict(
        orient="records"
    )
    goods_type = defaultdict(list)
    for good in goods_list:
        goods_type[good["Категория"]].append(good)
    return goods_type


def get_years(start_date):
    d1 = int(start_date)
    d2 = datetime.datetime.now().year
    x = d2 - d1
    if x % 10 == 1 and x != 11 and x % 100 != 11:
        return "{0} год".format(x)
    elif 1 < x % 10 <= 4 and x != 12 and x != 13 and x != 14:
        return "{0} года".format(x)
    else:
        return "{0} лет".format(x)


def render_page(data_goods, start_date):
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )
    feedback_desc = "Уже {0} с вами".format(get_years(start_date))
    template = env.get_template("template.html")
    rendered_page = template.render(
        feedback_desc=feedback_desc, goods_type=get_data(data_goods)
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def main():
    dotenv.load_dotenv()
    data_goods = os.getenv("EXCEL")
    start_date = os.getenv("START_DATE")
    render_page(data_goods, start_date)
    server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
