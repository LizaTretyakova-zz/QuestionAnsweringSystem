import unittest
import src.attributes as attributes

import sys
from os.path import dirname, abspath
#sys.path.insert(0, dirname(dirname(abspath(__file__))))
import database_utils


class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.downloads_wrapper = database_utils.DownloadsWrapper()
        self.customers_wrapper = database_utils.CustomersWrapper()

    def _test_downloads_success_(self, q: str, a: int) -> None:
        parsed_question = attributes.parse(q)
        wrapper_answer = self.downloads_wrapper.get(parsed_question)
        self.assertIsNotNone(wrapper_answer)
        # self.assertEqual(wrapper_answer['message'], 'Success')
        self.assertEqual(wrapper_answer['result'][0], a)

    def _test_customers_success_(self, q: str, a: int) -> None:
        parsed_question = attributes.parse(q)
        wrapper_answer = self.customers_wrapper.ask(parsed_question)
        self.assertIsNotNone(wrapper_answer)
        self.assertEqual(wrapper_answer, a)

    def test_amount_general(self):
        self._test_downloads_success_('How many downloads were made in total?', 2028)

    def test_amount_single_location(self):
        self._test_downloads_success_('how many downloads were there in Russia?', 766)
        self._test_downloads_success_('How many different products are downloaded from Russia?', 766)
        self._test_customers_success_('How many customers are there in United States of America?', 2)

    def test_amount_multiple_locations_downloads(self):
        self._test_downloads_success_('how many downloads were made in Russia and Germany?', 1966)

    def test_amount_multiple_locations_customers(self):
        self._test_customers_success_('how many customers were there in Russia and United Kingdom?', 2)
        # self._test_customers_success_('How many customers are there in North America?', 2)

    def test_downloads_wrapper_handles_upper_case_spelling(self):
        self._test_downloads_success_('How many downloads are there in European Union?', 1200)

    def test_customers_wrapper_handles_upper_case_spelling(self):
        self._test_customers_success_('How many customers are there in North America?', 2)

    def test_amount_time(self):
        self._test_downloads_success_('How many times PyCharm was downloaded in 2015?', 1262)
        self._test_downloads_success_('how many downloads were 1 year ago?', 1262)
        self._test_downloads_success_('How many downloads have been since 2015?', 1262)
        self._test_downloads_success_('Which number of clients downloaded PyCharm in 2014?', 766)  # 534?
        self._test_downloads_success_('How many downloads were from 2000 to 2016 except 2015?', 766)
        self._test_downloads_success_('How many downloads were till 2016 without 2015?', 766)
        self._test_downloads_success_('How many downloads were there within 2014 and 2015?', 2028)
        self._test_customers_success_('How many customers have been since 2000?', 4)
        self._test_customers_success_('How many customers were there in 2000 and 2011?', 0)
        self._test_customers_success_('How many customers were there in 2012?', 4)
        self._test_customers_success_('How many customers were there during 2012?', 4)

    def test_amount_location_time(self):
        self._test_downloads_success_('how many downloads were there in 2015?', 1262)
        self._test_downloads_success_('how many downloads were in Russia in 2014?', 766)
        # self._test_downloads_success_('how many downloads were there in Nigeria in 2014?', 0)
        # create one more test function to test zero values
        self._test_downloads_success_('How many downloads of PyCharm were made from Russia from 2013 to 2015?', 766)
        self._test_downloads_success_('How many downloads of PyCharm were made from Russia between 2013 and 2015?', 766)

        # What was the number of licences of PyCharm sold in Russia in 2014?
        # European Union 2 years ago

        self._test_customers_success_('How many customers were there in Russia in 2012?', 1)

    def draft_test_another_spelling(self):
        self._test_customers_success_('How many customers were there in 2012 in Russian Federation?', 1)
        self._test_customers_success_('How many customers are there in USA?', 2)
        # Spacy does not recognize USA vs United States of America, Russian Federation vs Russia, Netherlands & Holland,
        # but what it does recognize is UK & United Kingdom & Great Britain (not GB but never mind) and Suomi & Finland,
        # so we'll need to add these test data
        self._test_downloads_success_('How many downloads were there in 2012 in Finland?', 42)
        self._test_downloads_success_('How many downloads were there in 2012 in Suomi?', 42)
        # create test "test_equal_result"?.. TODO
        self._test_downloads_success_('How many downloads were there in 2012 in UK?', 43)
        self._test_downloads_success_('How many downloads were there in 2012 in United Kingdom?', 43)
        self._test_downloads_success_('How many downloads were there in 2012 in Great Britain?', 43)
