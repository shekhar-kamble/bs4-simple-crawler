import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
def get_img_list(url_list):
    crawl_list = []
    http_error = False
    for url in url_list:
        try:
            page = urllib2.urlopen(url).read()
            soup = BeautifulSoup(page)
            img_list = soup.findAll("img")
            img_list = [i.get("src","") for i in img_list]
            # img_list = validate_url(url,img_list)
            img_list = list(set(img_list))
            crawl_list = crawl_list + img_list
        except ValueError:
            pass
        except urllib2.HTTPError:
            http_error = True
        if len(crawl_list) == 0 and http_error:
            raise TypeError("Invalid url")
    return crawl_list
