from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

page = set()
random.seed(datetime.datetime.now())


# 获取页面中所有的内链链表
def getInternalLinks(bs, includeUrl):
    includeUrl = '{}://{}'.format(urlparse(includeUrl).scheme, urlparse(includeUrl).netloc)
    internalLinks = []

    # 找出所有以"/"开头的链接
    for link in bs.find_all('a', href=re.compile('^(/|.*' + includeUrl + ')')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if link.attrs['href'].startwith('/'):
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])

    return internalLinks


# 获取页面中所有外链的列表
def getExternalLinks(bs, excludeUrl):
    externalLinks = []

    # 找出所有以"http"或"www"开头且不包含当前URL的链接
    for link in bs.find_all('a',
                            href=re.compile('^(http|www)((?!' + excludeUrl + ').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])

    return externalLinks


# 随机获取一个外链
def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bs = BeautifulSoup(html, 'html.parser')
    externalLinks = getExternalLinks(bs, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links, looking around the site for one")
        domain = f"{urlparse(startingPage).scheme}://{urlparse(startingPage).netloc}"
        internalLinks = getInternalLinks(bs, domain)
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0,len(externalLinks)-1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print(f"Random external link is {externalLink}")
    followExternalOnly(externalLink)


followExternalOnly("http://orelly.com")
