import urllib2
from bs4 import BeautifulSoup
from urlparse import urlparse
def get_crawl_list(url_list, depth):
    crawl_list = []
    if depth <= 1:
        crawl_list = url_list
        return crawl_list
    else:
        depth = depth - 1
        for url in url_list:
            try:
                print url
                page = urllib2.urlopen(url).read()
                soup = BeautifulSoup(page)
                anchors_list = soup.findAll("a")
                anchors_list = [a.get("href","") for a in anchors_list]
                anchors_list = validate_urls(url,anchors_list)
                crawl_list = crawl_list + anchors_list
            except (ValueError, urllib2.HTTPError):
                pass
            # crawl_list = list(set(crawl_list))
    return get_crawl_list(crawl_list, depth)

def validate_urls(source_url, url_lists):
    base_url = urlparse(source_url).netloc
    url_lists = [url for url in url_lists if base_url in url]
    url_lists = list(set(url_lists))
    return url_lists