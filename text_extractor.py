#dfs not suitable, alter: level constraint added 
#tag category
#direct parent relation
from urllib.parse import urlparse
from urllib.parse import urljoin
import mechanicalsoup
from bs4 import BeautifulSoup
import sys
import io

sys.stdout=io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')

home="<Website-URL>"
url_que=[]
browser=mechanicalsoup.StatefulBrowser()
roof=1 #level top
file=open('content.txt', 'w', encoding='utf-8')

def is_absolute(url):
    return bool(urlparse(url).netloc)

def text_extract(page):
    try:
        soup = BeautifulSoup(str(page), features="html.parser")
    except:
        return
    for script in soup(["script", "style"]):
        script.extract() 

    tags=[]
    for tag in soup.find_all(string=True):
        if(len(tag.text.strip('\n')) > 1):
            tags.append(tag)

    content=[[tags[0], tag.text.strip()]]
    for i in range(1, len(tags)):
        tag=tags[i]
        if(tag.parent in content[-1][0].parents or content[-1][0].parent in tag.parents): #direct parent
            content[-1][1]+=' '+tag.text.strip() 
            if(tag.parent in content[-1][0].parents): #now >= past || else: now <= past
                content[-1][0]=tag
        else:
            line=[tag, tag.text.strip()]
            content.append(line)

    text=[]
    for line in content:
        text.append(line[0].parent.name+' : '+line[1])
        
    global file
    file.write('\n'.join(text))

def link_extract(url, page):

    try:
        links=[tag.get('href') for tag in page.find_all('a')]
    except:
        return

    for i in range(len(links)):
        if(not is_absolute(links[i])):
            links[i]=urljoin(url,links[i])

    return links

def is_external(url):
    keywords=['instagram', 'twitter', 'tiktok', 'facebook', 'youtube', 'apple', 'google']
    for word in keywords:
        if(word in url):
            return True
    return False

def url_explore(url, level):
    if(level > roof):
        return
    url_que.append(url)
    print(len(url_que), url)#

    try:
        browser.open(url)
    except:
        return
    page=browser.page
    text_extract(page)
    links=link_extract(url, page)

    if(links):
        for i in range(len(links)):
            if(not links[i] in url_que ):
                if(not is_external(links[i])):
                    url_explore(links[i], level+1)

url_explore(home, 0)
