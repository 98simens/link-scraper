from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
import threading
from bs4 import BeautifulSoup as bfs
import requests
import re
import urllib.parse as ulp
import scraper
from kivy.config import Config

Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '600')

class LinkScraper(Widget):
    def addResultRow(self, url, statusCode, responseTime):
        resultLayout = self.ids['resultLayout']
        resultLayout.rows += 1

        rowLayout = BoxLayout(orientation= 'horizontal', size=(resultLayout.width, 20), size_hint_y= None)
        rowLayout.add_widget(Label(text= url, size_hint= (.7, 1), text_size= (rowLayout.width * .7, 20)))
        rowLayout.add_widget(Label(text= str(statusCode), size_hint= (.15, 1), text_size= (rowLayout.width * .15, 20)))
        rowLayout.add_widget(Label(text= str(int(responseTime * 1000)) + ' ms', size_hint= (.15, 1), text_size= (rowLayout.width * .15, 20)))
        resultLayout.add_widget(rowLayout)

    def scrapeUrls(self, **kwargs):
        print('Starting...')
        start_url = ulp.urlparse(kwargs['url'])
        result = scraper.evaluateUrl(start_url.geturl())

        if(result):
            linkData = [{
                'url': start_url, 
                'html': result[0], 
                'request': result[1]
                }]
            checkedUrls = [start_url.geturl()]

            for link in linkData:
                foundUrls = scraper.getUrls(link['url'].geturl(), link['html'])
                for foundUrl in foundUrls:
                    if(foundUrl.geturl() in checkedUrls):
                        continue

                    if(start_url.hostname != foundUrl.hostname):
                        loadHtml = False
                    else:
                        loadHtml = True
                    html, pageRequest = scraper.evaluateUrl(foundUrl.geturl(), loadHtml)

                    if(html):
                        if(pageRequest.status_code < 300):
                            linkData.append({
                                'url': foundUrl,
                                'html': html,
                                'request': pageRequest
                            })
                    if(pageRequest):
                        self.addResultRow(foundUrl.geturl(), pageRequest.status_code, pageRequest.elapsed.total_seconds())
                    else:
                        self.addResultRow(foundUrl.geturl(), 'Timeout', 0)
                    checkedUrls.append(foundUrl.geturl())

        print('Done!')


    def startAnalyzeThread(self):
        url = str(self.ids['urlInput'].text)
        resultLayout = self.ids['resultLayout']
        resultLayout.clear_widgets()
        resultLayout.rows = 1 
        
        threading.Thread(target= self.scrapeUrls, kwargs={'url': url}).start()

class LinkScraperApp(App):
    def build(self):
        return LinkScraper()


if __name__ == '__main__':
    LinkScraperApp().run()