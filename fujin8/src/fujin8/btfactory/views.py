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
from django.shortcuts import get_object_or_404
import string
import hashlib

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
    reobj = re.compile(u"^★㊣最新の[(日本)(亚洲)](.)*♂(.)*♀$")
        
    for link in links:            
        content = link.getText()                
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
            if count > 14:
                #only parse 15 links every time
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
    
    parsed_daily_list = DailyLink.objects.filter(parsed=False).order_by('-id')[:100]
    t = loader.get_template('btfactory/daily.html')
    c = Context({'parsed_daily_list': parsed_daily_list,'parsed_count':count,})
    return HttpResponse(t.render(c))


def dailymovie(request, daily_id):    
    
    dl = get_object_or_404( DailyLink, pk=daily_id)
    try:
        page = urllib2.urlopen(dl.link)
        content = page.read()         
        content = content.decode('gb18030').encode('utf8')
        page.close() 
    except URLError:        
        raise
    
    index = content.find("<div id=\"content\">")+18
    index2 = content.find("</div>",index)
    content = content[index:index2]    
    movies = content.split("<br />\r\n<br />\r\n")
    mi = 1    
    movielinks = []    
    p = re.compile('<IMG class="postimg" src=".*" />',re.IGNORECASE);
    for movie in movies:
        logger.info("movie "+str(mi)+" :\n" + movie)
        logger.info("movie "+str(mi)+"***************************************************************")
        mi = mi + 1          
        movie = movie.strip()
        if len(movie) < 20:
            continue
        #create the movielink object
        digestkey = hashlib.sha224(movie).hexdigest()
        tIndex = movie.find("<br />")
        mTitle = movie[0:tIndex] 
        #find all images        
        
        images = []
        for match in p.finditer(movie):
            image = str(match.group())
            iIndex = image.find('src="')+5
            iIndex2 = image.find('"',iIndex)            
            image = image[iIndex:iIndex2]
            #logger.info("movie: "+mTitle+" image:"+image)
            images.append(image)
            
        imagesLink = ";".join(images)
        ml = MovieLink(title=mTitle,raw_desc=movie,digestkey=digestkey,daily_link=dl,images=imagesLink)
        try:
            ml.save()
            movielinks.append(ml)
        except IntegrityError:
            logger.info("movie already existed:...." + mTitle)
            pass    
        
    movielinks = MovieLink.objects.filter(parsed=False,daily_link=dl).order_by('-id')[:100]    
    t = loader.get_template('btfactory/dailymovies.html')
    c = Context({'dl':dl,'movielinks':movielinks})
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
