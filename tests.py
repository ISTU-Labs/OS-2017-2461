from crawler import CrawlerModel, CurrencyStorer, Exporter
# from nose.tools import SkipTest


# @SkipTest
# class TestCrawler:
#     def setUp(self):
#         self.crawler = CrawlerModel()

#     def test_run(self):
#         rc = self.crawler.cbr()
#         assert len(rc) > 0


class TestStorer:
    def setUp(self):
        self.crawler = CrawlerModel()
        self.cur_list = self.crawler.cbr()
        self.store = CurrencyStorer("teststore.db")
        self.exporter = Exporter("a.xml")

    def test_storer(self):
        assert self.store.length() == 0
        self.store.store(self.cur_list)
        assert self.store.length() > 0

    def test_to_xml(self):
        assert self.exporter.export(self.cur_list)

    def tearDown(self):
        self.store._clean()
