import requests
import urllib
import queue
import re
import time
import random
import datetime
import json
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from bs4.element import Comment
import warnings
warnings.filterwarnings('ignore')

class GoogleCrawler():
    
    def __init__(self):
        self.url = 'https://www.google.com/search?q='
        self.next_page_queue = queue.Queue()
        self.last_page = 0

    def get_source(self,url):
        try:
            session = HTMLSession()
            headers = {
                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
                "accept-language": "zh-TW;q=0.5,en-US;q=0.5",
                "cache-control": "max-age=0",
                "referer": "https://www.google.com/",
                "upgrade-insecure-requests": "1",
                "dnt": "1",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "sec-gpc": "1"
            }
            response = session.get(url, headers=headers, verify=False, timeout=10)
            if response.status_code != 200:
                #print("Status Code : ", response.status_code)
                if response.status_code == 429:
                    return 1
                return 2
            return response
        except requests.exceptions.RequestException as e:
            #print(e)
            return 0

    def main_search(self, date=None):
        err = 0
        result = []
        if date:
            url = "https://www.google.com/search?q=\"Applied+Material\"+OR+ASML+OR+SUMCO+TSMC+-filetype:pdf&tbs=cdr:1,cd_min:{month}/{day}/{year},cd_max:{month}/{day}/{year}&filter=0".format(month=date.month, day=date.day, year=date.year)
        else :
            url = "https://www.google.com/search?q=\"Applied+Material\"+OR+ASML+OR+SUMCO+TSMC+-filetype:pdf&tbs=qdr:d&filter=0"
        print('URL : {url}'.format(url=url))
        response = self.get_source(url)
        if response == 0 or response == 1 or response == 2:
            err = response
            return result, err
        self.parse_nextPage(response)
        result += self.parse_googleResults(response)
        if self.next_page_queue.empty():
            return result, err
        while True:
            url = 'https://www.google.com' + self.next_page_queue.get()
            print('[Check][URL] URL : {url}'.format(url=url))
            if self.next_page_queue.empty():
                response = self.get_source(url)
                if response == 0 or response == 1 or response == 2:
                    err = response
                    return result, err
                self.parse_nextPage(response)
                result += self.parse_googleResults(response)
                if self.next_page_queue.empty():
                    break
                    
            response = self.get_source(url)
            if response == 0 or response == 1 or response == 2:
                err = response
                return result, err
            result += self.parse_googleResults(response)
            #time.sleep(random.randint(3,20))
        print("*" * 20 + "Crawler Done!" + "*" * 20)
        return result, err
        
    def parse_nextPage(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll('a', attrs={"aria-label": re.compile(r"Page \d+")})
        for result in results:
            if self.last_page < int(result['aria-label'][-2:]):
                self.next_page_queue.put(result['href'] + "&filter=0")
                self.last_page = int(result['aria-label'][-2:])
                
    def parse_googleResults(self,response):
        css_identifier_result = "tF2Cxc"
        css_identifier_link = "yuRUbf"
        css_identifier_date = "MUxGbd"
            
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            date = result.find("span", {"class": css_identifier_date})
            if date == None:
                continue
            item = {
                'link': result.find("div", {"class": css_identifier_link}).find(href=True)['href']
            }
            output.append(item)
        return output
    
    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element,Comment):
            return False
        return True

    def text_from_html(self, body):
        soup = BeautifulSoup(body, 'html.parser')
        texts = soup.findAll(text=True)
        visible_texts = filter(self.tag_visible, texts)  
        return u" ".join(t.strip() for t in visible_texts)

    def keyword_count(self, text):
        tsmc = text.count('TSMC') + text.count('台積電') + text.count('臺積電')
        asml = text.count('ASML') + text.count('艾思摩爾')
        am = text.count("Applied Material") + text.count('應用材料')
        sumco = text.count('SUMCO') + text.count('勝高')
        return tsmc, asml, am, sumco
    
    def url_to_count(self, urls):
        count_result = {'TSMC' : 0, 'ASML' : 0, 'AM':0, 'SUMCO':0}
        for url in urls:
            response = self.get_source(url['link'])
            if response == 0 or response == 1 or response == 2 :
                continue
            orignal_text = self.text_from_html(response.text)
            tsmc, asml,am,sumco = self.keyword_count(orignal_text)
            count_result['TSMC'] += tsmc
            count_result['ASML'] += asml
            count_result['AM'] += am
            count_result['SUMCO'] += sumco    
        return count_result
    
    def write_result(self, date, result, path=None):
        date = datetime.datetime.strftime(date, "%Y-%m-%d")
        count_result = self.url_to_count(result)
        if path :
            with open(path + '/' + date + '.json', 'w') as f:
                json.dump(count_result, f)
                print(date, " : ", count_result)
        else:
            return count_result
        print("*" * 20 + "Counting Done!" + "*" * 20)

    def check_search_valid(self):
        test_url = "https://www.google.com/search?q=ASML+OR+SUMCO+TSMC&tbs=cdr:1,cd_min:5/3/2022,cd_max:5/3/2022&filter=0"
        response = self.get_source(test_url)
        if response == 1:
            return True 
        return False

