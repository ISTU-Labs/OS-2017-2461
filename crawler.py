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
        cur.execute("COMMIT")

    def length(self):
        cur = self.conn.cursor()
        answer = cur.execute("""
             SELECT count(*) as CNT FROM rate
        """)

        for row in answer:
            cnt = row[0]
            return cnt

    def _clean(self):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM rate")
        cur.execute("COMMIT")


class Exporter(object):
    def __init__(self, filename):
        self.filename = filename

    def export(self, curs):
        root = etree.Element("root")
        for code, val in curs:
            c = etree.SubElement(root, "cur", {"id": str(code)})
            c.text = "{:.5f}".format(val)

        doc = etree.ElementTree(root)
        doc.write(self.filename,
                  pretty_print=True,
                  xml_declaration=True,
                  encoding="utf-8")

        return True
