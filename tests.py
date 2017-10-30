from crawler import CrawlerModel, CurrencyStorer
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

    def test_storer(self):
        self.store.store(self.cur_list)

    def tearDown(self):
        self.store._clean()
