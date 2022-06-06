import pytest
import datetime
from header.crawler import GoogleCrawler


def test_main_search_with_date():
    crawler = GoogleCrawler()
    date = datetime.datetime(2022, 1, 1, 0, 0)
    results, err = crawler.main_search(date)
    assert len(results) > 0 and err == 0

def test_main_search_without_date():
    crawler = GoogleCrawler()
    results, err = crawler.main_search()
    assert len(results) > 0 and err == 0

def test_get_source():
    crawler = GoogleCrawler()
    target_url = 'https://www.reuters.com/technology/exclusive-ukraine-halts-half-worlds-neon-output-chips-clouding-outlook-2022-03-11/'
    response = crawler.get_source(target_url)
    assert response.status_code == 200

def test_parse_nextPage():
    crawler = GoogleCrawler()
    target_url = 'https://www.google.com/search?q=tsmc'
    response = crawler.get_source(target_url)
    crawler.parse_nextPage(response)
    assert crawler.next_page_queue.qsize() > 0

def test_parse_googleResults():
    crawler = GoogleCrawler()
    target_url = 'https://www.google.com/search?q=tsmc'
    response = crawler.get_source(target_url)
    result = crawler.parse_googleResults(response)
    assert len(result) > 0

