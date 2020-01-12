import urllib
import requests
from bs4 import BeautifulSoup
from idlelib import browser
from urllib.request import urlopen
import mechanicalsoup
from threading import Thread
import  time
import itertools
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework import serializers
from rest_framework import viewsets

from selenium.webdriver.chrome.service import Service

from crawller.serializers import UserSerializer, GroupSerializer

exploreLink=[]
links = []
formats=['jpg','exe','pdf','apk','mp4','mp3','jpeg','png','rar','aspx']


def readRobots(url):

    try:
        data = urlopen(url+'/robots.txt')
    except Exception as e:
        print("Exepte to open robots",e)
        data=None
        pass

    robotLink =set()
    if data:
        for line in data:
            line=line.decode("utf-8")
            str_list=str(line).split(":")
            if str_list[0].lower() == "disallow":
                robotLink.add(url+str_list[1].strip().rstrip('/'))
    return robotLink

def siteMapCrawl(url,link):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(link)
    exploreLink.append(link)
    aTags=browser.links()
    for tag in aTags:
        href=tag['href']
        if href.startswith(url):
            if href[-1] == "/":
                href = href[:-1]
            if href not in exploreLink:
                exploreLink.append(href)
        if href.startswith('/'):
            href=str(url)+str(href)
            if href not in exploreLink:
                exploreLink.append(href)
def str_to_bool(s):
    if s == 'True' or s=='true':
         return True
    elif s == 'False' or s=='false':
         return False
    else:
         raise ValueError
@api_view(["POST"])
def crawl(request):
    data=request.data
    url=data["url"]
    t=str_to_bool(data["t"])
    robotLink=readRobots(url)
    links.append(url)
    siteMapLink=set()
    index=0;
    if robotLink and url in robotLink:
        robotLink.remove(url)

    if t:
        r = requests.get(url+"/sitemap.xml")
        xml = r.text
        soup = BeautifulSoup(xml)
        sitemapTags = soup.find_all("sitemap")
        print(sitemapTags)
        for sitemap in sitemapTags:
            loc=sitemap.findNext("loc").text
            loc=loc.replace('/sitemap','')
            siteMapLink.add(loc)
        for link in siteMapLink:
            siteMapCrawl(url,link)
    else:
        while links:
            link=links[0]
            index=index+1
            print("kodom linko daram expelore mikonm",link)
            try:
                if(index%100==0):
                    time.sleep(1)
                if link not in exploreLink and link not in robotLink:
                    getLinks(url,link)
                    links.remove(link)
            except Exception as e:
                links.remove(link)
                print("link",link)
                print("exeptions",e)
                continue
#        return render(request, 'crawl.html', {'links':exploreLink})
    return  Response(exploreLink)
def readRobotFromHtml(link):
    webpage = urlopen(str(link)).read()
    soup = BeautifulSoup(webpage, "lxml")
    robots = soup.find_all("meta")
    for robot in robots:
        if robot.get("name", None) == "robots":
            content=str(robot.get("content",None)).lower()
            if 'nofollow' in content:
                return False
        else:
            return True
def getLinks(url,link):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open(link)
    allowToCrawl=readRobotFromHtml(link)
    exploreLink.append(link)
    if allowToCrawl:
        aTags=browser.links()
        if aTags:
            for tag in aTags:
                href=tag['href']
                href_part=str(href).split('.')
                if href_part[-1].lower() not in formats:
                    admision=True
                else:
                    admision=False
                if admision:
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
    print("links should visit count",len(links))
    print("expelored count",len(exploreLink))

def form(request):

    url="http://lms.ui.ac.ir"
    # browser = mechanicalsoup.StatefulBrowser()
    # browser.open(url)
    # form = browser.select_form()
    # form.print_summary()
    # browser["username"] = "953611133039"
    # browser["password"] = "1272508171"
    # response = browser.submit_selected()
    # browser.launch_browser()
    #driver= webdriver.firefox('127.0.0.1:8000/test/test')

    return render(request, 'form.html', {})

@api_view(["POST"])
def calctest(x1):
    try:
        print(x1)
        x=json.loads(x1.body)
        print(x)
        return JsonResponse({'num': 12})
    except ValueError as e:
        return Response(e.args[0],status.HTTP_400_BAD_REQUEST)
@api_view(["GET"])
def gettest(t):
    return JsonResponse({'num':12})

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer