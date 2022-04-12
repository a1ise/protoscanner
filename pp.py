from selenium import webdriver
from selenium.webdriver.chrome.service import Service as sv
from selenium.webdriver.chrome.options import Options
import sys
import time
from urllib.parse import *

class ppscanner:

    def __init__(self):    
        options = Options()
        options.binary_location = ''
        service = sv(executable_path='./chromedriver')
        options.add_argument('--headless')
        self.payloads = [
            '?__proto__[KikkaKurabe]=KikkaKurabe',
            '?__proto__.KikkaKurabe=KikkaKurabe',
            '#__proto__[TerutoKurabe]=TerutoKurabe',
            '#__proto__.TerutoKurabe=TerutoKurabe',
        ]   
        self.driver = webdriver.Chrome(service=service, options=options)

    def scan(self, url):
        for payload in self.payloads:
            newUrl = self.urlParamAppend(url, payload)
            self.driver.set_page_load_timeout(15)
            time.sleep(2)
            try:
                self.driver.get(newUrl)
            except Exception as e:
                continue
            result = self.driver.execute_script('return Object.prototype.KikkaKurabe !== undefined || Object.prototype.TerutoKurabe !== undefined || Object.prototype.KikkaKurabe === "KikkaKurabe" || Object.prototype.TerutoKurabe === "TerutoKurabe"')
            if result:
                print("Found!!!  Vlunerable webpage\n   ->"+url+payload)

    def urlParamAppend(self, oldUrl, payload):
        parseUrl = urlparse(oldUrl)
        newUrl = parseUrl.scheme+ '://' + parseUrl.hostname + parseUrl.path
    
        if payload[0] == '?':
            newUrl = newUrl + payload + parseUrl.query + '#' + parseUrl.fragment
        else:
            newUrl = newUrl + '?' + parseUrl.query + payload + parseUrl.fragment
        
        return newUrl

    def quit(self):
        self.driver.quit()
    
def main():
    scanner = ppscanner()
    if sys.argv[1] == "-t":
        mode = 'text'
        text = sys.argv[2]
    else:
        mode = 'url'
        url = sys.argv[1]

    if mode == 'url':
        scanner.scan(url)
    else:
        with open(text, 'r') as f:
            while True:
                url = f.readline()
                if not url:
                    break
                scanner.scan(url)
    
    scanner.quit()

main()