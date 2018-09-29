from bs4 import BeautifulSoup as bfs
import requests
import re
import urllib.parse as ulp



#with open('test_documents/test1.html') as html:
#    data = bfs(html, features="html5lib")
START_URL = ulp.urlparse('https://www.stormfors.se/')
pages = [START_URL.geturl()]
links = [START_URL.geturl()]
i = 0
for page in pages:
    print('--------------------' + page + '--------------------')
    print('Analyzed: ' + str(i))
    page_data = requests.get(page)
    data = bfs(page_data.text, features="html5lib")

    for elem in data.find_all('a', href=re.compile('.+')):
        link = ulp.urlparse(elem['href'])
        if not(link.scheme):
            #src = page_data.url.rsplit('#',1)[0].strip('/')
            #path = link.rsplit('#',1)[0]
            joined_link = ulp.urljoin(page_data.url, link.geturl()).rsplit('#',1)[0]
            link = ulp.urlparse(joined_link)
            
        file_ext = link.path.rsplit('.', 1)
        if(len(file_ext) > 1):
            if(not file_ext[1].lower() in ('html', 'php', 'asp', 'aspx')):
                continue
        if(not link.geturl() in links):
            try:
                response = requests.head(link.geturl())
            except (requests.exceptions.MissingSchema, requests.exceptions.InvalidSchema):
                continue

            if(response.status_code < 300):
                if(START_URL.hostname == link.hostname):
                    pages.append(link.geturl())
                links.append(link.geturl())
                #print('LINK: ' + link.geturl())
                #print('RESPONSE: ' + str(response.status_code))
                print('Pages to analyze:' + str(len(pages) - i))
                print('Links collected:' + str(len(links)))
                print('-----------------------------------------------------------')
    i += 1

