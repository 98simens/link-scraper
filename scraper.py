from bs4 import BeautifulSoup as bfs
import requests
import re
import urllib.parse as ulp

def validateHref(href, url):
    link = ulp.urlparse(href.rstrip('/'))
    if not(link.scheme):
        if(':' in href):
            return False
        joined_link = ulp.urljoin(url, link.geturl()).rsplit('#',1)[0]
        link = ulp.urlparse(joined_link.rstrip('/'))
    if(link.scheme != 'http'):
        return False
    return link

def getUrls(originUrl, html):
    data = bfs(html, features="html5lib")

    urls = []
    for elem in data.find_all('a', href=re.compile('.+')):
        href = elem['href']
        url = validateHref(href, originUrl)
        if(url and url.geturl() not in urls):
            urls.append(url)
    return urls

def evaluateUrl(url, loadHtml = True):
    try:
        pageRequest = requests.get(url, stream=True, timeout=15)
    
        if(pageRequest.encoding is None):
            pageRequest.encoding = 'UTF-8'
        if('text/html' in pageRequest.headers['content-type'] and loadHtml):
            html = ""
            for line in pageRequest.iter_lines(decode_unicode=True):
                if line:
                    html += line
            return html, pageRequest
        else:
            return False, pageRequest
    except requests.exceptions.ConnectionError:
        return False, False

