from django.shortcuts import render
from bs4 import BeautifulSoup
from idlelib import browser
import mechanicalsoup
from threading import Thread
import  time
from urllib.request import urlopen
import urllib.robotparser
import itertools
exploreLink=[]
links = []



def crawlAll(request):
    url="http://lms.ui.ac.ir"
    link="http://lms.ui.ac.ir"
    getAllLink(url,link)
    return render(request, 'allTag.html', {'links':links})

def readRobots(url):
    data = urllib.request.urlopen(url+'/robots.txt')
    robotLink = []
    for line in data:
        line=line.decode("utf-8")
        str_list=str(line).split(":")
        if str_list[0].lower() == "disallow":
            robotLink.append(url+str_list[1].strip().rstrip('/'))
    return  robotLink

def crawl(request):
    url="http://lms.ui.ac.ir"
    robotLink=readRobots(url)
    links.append(url)
    index=0;
    while links:
        link=links[0]
        index=index+1
        try:
            if(index%100==0):
                time.sleep(1)
            if link not in exploreLink:
                getLinks(url,link)
                links.remove(link)
        except Exception as e:
            links.remove(link)
            print("link",link)
            print("exeptions",e)
            continue
    return render(request, 'crawl.html', {'links':list(itertools.chain.from_iterable(zip(links, exploreLink)))})

def getLinks(url,link):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(link)
    aTags=browser.links()
    if aTags:
        for tag in aTags:
            href=tag['href']
            if href.startswith(url):
                if href[-1] == "/":
                    href = href[:-1]
                if href not in links:
                    if href not in exploreLink:
                        links.append(href)
            if href.startswith('/'):
                href = str(url)+str(href)
                if href[-1] == "/":
                    href = href[:-1]
                if href not in links:
                    if href not in exploreLink:
                        links.append(href)
    exploreLink.append(link)
    print("links should visit count",len(links))
    print("expelored count",len(exploreLink))

def getAllLink(url,link):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(link)
    aTags = browser.links()
    for tag in aTags:
        href = tag['href']
        allLink.append(href)
    print(len(allLink))

def form(request):
    url="http://lms.ui.ac.ir"
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(url)
    form = browser.select_form()
    form.print_summary()
    form.set_input({"login": username, "password": password})
    form.choose_submit('submit')
    return render(request, 'form.html', {'form':form})