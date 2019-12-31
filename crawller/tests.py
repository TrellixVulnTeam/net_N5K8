from django.test import TestCase
from urllib.request import urlopen
import urllib.robotparser

# Create your tests here.
def readRobots( url="http://lms.ui.ac.ir/robots.txt" ):
    links=[]
    data = urllib.request.urlopen(url)
    print(type(data))
    for line in data:
        print(line )
        line=line.decode("utf-8")
        str_list=str(line).split(":")
        if str_list[0].lower() == "disallow":
            links.append(str_list[1].strip())
    return links
print(readRobots())