import requests
import datetime
from lxml import etree
from io import BytesIO
import sqlite3
import pprint

CBR_URI = 'http://www.cbr.ru/scripts/XML_daily.asp'


class CrawlerModel(object):
    def __init__(self):
        self.currencies = []

    def cbr(self, date=None):
        if date is None:
            date = datetime.datetime.now()
        r = requests.get(CBR_URI)
        c = r.content
        i = BytesIO(c)
        tree = etree.parse(i)

        cs = self.currencies = []
        root = tree.getroot()
        for i in range(len(root)):
            rec = root[i]
            print(etree.tostring(rec, pretty_print=True, encoding=str))

            cs.append(
                (int(rec[0].text),
                 float(rec[4].text.replace(",", "."))))
        # pprint.pprint(cs)
        return self.currencies


class CurrencyStorer(object):
    def __init__(self, filename):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.check_structures()

    def check_structures(self):
        cur = self.conn.cursor()
        cur.execute("""
           CREATE TABLE IF NOT EXISTS rate (
              cur_id int,
              date   date,
              rate   float
           )
        """)

    def store(self, cur_list, date=None):
        if date is None:
            date = datetime.datetime.now()
        cur = self.conn.cursor()
        new_cur_list = ((r[0], date, r[1]) for r in cur_list)
        cur.executemany("INSERT INTO rate VALUES (?, ?, ?)", new_cur_list)

    def _clean(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM rate")
