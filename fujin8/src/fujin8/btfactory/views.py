#coding=utf-8 
from btfactory.models import MovieLink, DailyLink, MonthlyLink
from django.template import loader
from django.template.context import Context
from django.http import HttpResponse
import urllib2
import logging
from BeautifulSoup import BeautifulSoup,Tag
import re
import urlparse
from django.db.utils import IntegrityError
from urllib2 import URLError

logger = logging.getLogger(__name__)

def index(request):
    
    latest_movies_list = MovieLink.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('btfactory/index.html')
    c = Context({
        'latest_movies_list': latest_movies_list,
    })
    return HttpResponse(t.render(c))

# parse daily record by the monthly link
def parseMonth(month_url):
    logger.info("Parse Month:" + str(month_url.link))
    url = urlparse.urlsplit(month_url.link)
    servername = url[0]+"://"+url[1]    
    try:
        page = urllib2.urlopen(month_url.link)
    except URLError:        
        raise
    soup = BeautifulSoup(page,fromEncoding='gbk')
    #content = soup.prettify()
    links = soup.findAll('a', {'href':True,'target':True},True)
    
    count = 0
    parsed_count = 0
    for link in links:            
        content = link.getText()        
        reobj = re.compile(u"^★(.)*♂(.)*♀$")
        match = reobj.search(content)
        if match:
            count = count+1
            logger.info(content)
            #存储日常链接            
            linkstr = servername+link.get('href','')
            dailyLink = DailyLink(link=linkstr,monthly_link=month_url,label=content)
            try:
                dailyLink.save()
                parsed_count = parsed_count + 1
            except IntegrityError:
                logger.info("URL already existed:...." + linkstr)
                pass    
            if count > 4:
                #only parse 5 links every time
                break 
        else:
            logger.info(content+" not match!")
            continue
    return parsed_count   
     
def daily(request):    
    links = MonthlyLink.objects.filter(enable=True)
    count = 0
    for link in links:
        count = count + parseMonth(link)
    
    parsed_daily_list = DailyLink.objects.filter(parsed=False)[:100]
    t = loader.get_template('btfactory/daily.html')
    c = Context({'parsed_daily_list': parsed_daily_list,'parsed_count':count,})
    return HttpResponse(t.render(c))

def dailymovie(request):
    parsed_movie_list = MovieLink.objects.filter(parsed=False)[:100]
    t = loader.get_template('btfactory/index.html')
    c = Context({'parsed_movie_list': parsed_movie_list,})
    return HttpResponse(t.render(c))

def actress(request):

    latest_movies_list = MovieLink.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('btfactory/index.html')
    c = Context({
        'latest_movies_list': latest_movies_list,
    })
    return HttpResponse(t.render(c))

def actressinfo(request):

    latest_movies_list = MovieLink.objects.all().order_by('-pub_date')[:5]
    t = loader.get_template('btfactory/index.html')
    c = Context({
        'latest_movies_list': latest_movies_list,
    })
    return HttpResponse(t.render(c))
