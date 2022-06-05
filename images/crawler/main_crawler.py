import datetime
import warnings
from header.crawler import GoogleCrawler
warnings.filterwarnings('ignore')

def get_history():
    date = datetime.datetime(2022,4,30,0,0)
    end = datetime.datetime(2022,5,1,0,0)
    while True:
        crawler = GoogleCrawler()
        print(datetime.datetime.strftime(date, "%Y-%m-%d"))
        if date == end :
            break
        result, err = crawler.main_search(date)
        if err == 1:
            time.sleep(4000)
            while crawler.check_search_valid():
                time.sleep(300) 
            continue
        crawler.write_result(date, result, path)    
        #time.sleep(random.randint(3,20))

        date += datetime.timedelta(days=1)


def get_today():
    today = datetime.datetime.today()
    crawler = GoogleCrawler()
    result, err = crawler.main_search()
    if err == 1:
        print("Too many request!")
        return 
    return crawler.write_result(today, result)


if __name__ == "__main__":
    get_today()
