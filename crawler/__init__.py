from crawler_get import get_crawl_list
from crawler_set import get_img_list
def crawl(url,depth):
    result = {}
    url_list = get_crawl_list([url],depth)
    img_list = []
    try:
        img_list = get_img_list(url_list)
    except TypeError:
        result["error"] = "Invalid url"
    except Exception:
        result["error"] = "bad crawl"
    result["len"] = len(img_list)
    result["images"] = img_list
    return result