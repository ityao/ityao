#coding=utf-8 
from btfactory.models import MovieLink, DailyLink, MonthlyLink, Actress
from django.template import loader
from django.template.context import Context, RequestContext
from django.http import HttpResponseRedirect
import urllib2
import logging
from BeautifulSoup import BeautifulSoup,Tag
import re
import urlparse
from django.db.utils import IntegrityError
from urllib2 import URLError
from django.shortcuts import get_object_or_404, render_to_response
import string
import hashlib

import datetime
import time
import cStringIO
from django.utils.encoding import smart_str, smart_unicode
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

logger = logging.getLogger(__name__)

def save_acttress_header(actress_id, original_location):
    
    from django.conf import settings
    import os
    
    opener1 = urllib2.build_opener()
    page1 = opener1.open(original_location)
    my_picture = page1.read()
    
    filename = settings.MEDIA_ROOT + "images/headers/"
    try:
        os.makedirs(filename)
    except OSError:
        pass 
     
    filename = filename + str(actress_id) + original_location[-4:]
    fout = open(filename, "wb")
    fout.write(my_picture)
    fout.close()
    
    urldir = settings.MEDIA_URL + "images/headers/" + str(actress_id) + original_location[-4:]   
    return urldir

#640 is iphones
def create_resized_image(image_name, original_location, xconstrain=640):
    
    from PIL import Image, ImageOps
    import os
    from django.conf import settings

    # Ensure a resized image doesn't already exist in the default MEDIA_ROOT/images/resized (MEDIA_ROOT is defined in Django's settings)
    month = str(datetime.date.today())[0:7]
    
    # 'dir' is a buildin function, so renam as 'monthly_dir'
    monthly_dir = '%simages/%s' % (settings.MEDIA_ROOT,month)
    try:
        os.makedirs(monthly_dir)
    except OSError:
        pass    
    filename = '%s/%s.jpg' % (monthly_dir, image_name)
    if not os.path.exists(filename): 
        # Fetch original image
        urllink = smart_str(original_location)
        imgdata = urllib2.urlopen(urllink).read()
        '''
        unsized_image1 = urllib.urlretrieve(urllink) 
        # Load the fetched image
        unsized_image = Image.open(unsized_image1[0])
        '''
        unsized_image = Image.open(cStringIO.StringIO(imgdata))
        # Create a resized image by fitting the original image into the constrains, and do this using proper antialiasing
        width, height = unsized_image.size
        if width > xconstrain: 
            yconstrain = int(xconstrain*height/width)
        else:
            xconstrain = width
            yconstrain = height           
        resized_image = ImageOps.fit(unsized_image, (xconstrain, yconstrain), Image.ANTIALIAS)
        # PIL sometimes throws errors if this isn't done
        resized_image = resized_image.convert("RGB") 
        # Save the resized image as a jpeg into the MEDIA_ROOT/images/resized
        resized_image.save(filename, 'jpeg')
         
    urldir = '%simages/%s' % (settings.MEDIA_URL,month)    
    return '%s/%s.jpg' % (urldir, image_name)

def index(request):
    
    latest_movies_list = MovieLink.objects.all().order_by('-pub_date')[:5]

    return render_to_response('btfactory/index.html', locals())

#从每日的新剧作页面读取剧作
def parseDailyMovie(dl):
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
    p = re.compile('<IMG class="postimg" src=".*" />',re.IGNORECASE);
    pl = re.compile('<A href=".*" target=_blank >\*\*\*\*\*點此下載\*\*\*\*\*</A>',re.IGNORECASE);
    for movie in movies:
        #logger.info("movie "+str(mi)+" :\n" + movie)
        #logger.info("movie "+str(mi)+"***************************************************************")
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
        
        dls = []
        for match in pl.finditer(movie):
            dlink = str(match.group())
            iIndex = dlink.find('href="')+6
            iIndex2 = dlink.find('"',iIndex)            
            dlink = dlink[iIndex:iIndex2]
            dls.append(dlink)            
        dlLinks = ";".join(dls)
        
        
        result = MovieLink.objects.filter(digestkey=digestkey)               
        if len(result) == 0:              
            ml = MovieLink(title = mTitle,raw_desc = movie,digestkey = digestkey,daily_link=dl,images=imagesLink,downloadlink=dlLinks)            
            ml.save()            
        else:
            logger.info("movie already existed:...." + mTitle)             
    dl.parsed = True
    dl.save()
    
# parse daily record by the monthly link
def parseMonth(month_url):
    #logger.info("Parse Month:" + str(month_url.link))
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
            if count > 3:
                #only parse 2 links every time
                break 
        else:
            logger.info(content+" not match!")
            continue
    return parsed_count   

def moviethumbcron(request):
    #get 1 link of not saved
    movielinks = MovieLink.objects.filter(images_loaded=False)[:5]
    #save image to local
    for ml in movielinks:
        images = ml.images.split(";")
        count = 0   
        imageLinks = [] 
        for image in images:
            count = count + 1
            imgname = str(ml.digestkey)+"_"+str(count)
            try: 
                link = create_resized_image(imgname, image)
                imageLinks.append(link) 
            except IOError:        
                continue
        ml.images = ";".join(imageLinks)
        ml.images_loaded = True
        ml.save()
    
    return render_to_response('btfactory/movie.html', locals())

def dailycron(request):
    # get daily link from the month link
    link = MonthlyLink.objects.get(enable=True)
    parseMonth(link)    
    # get movies from daily link page
    daily_lists = DailyLink.objects.filter(parsed=False).order_by('-id')[:100]
    for dl in daily_lists:
        parseDailyMovie(dl)
    
    return render_to_response('btfactory/dailycron.html', {'daily_lists': daily_lists})

def parseActress(url):
    try:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page)
        #content = content.decode('gb18030').encode('utf8')
        page.close() 
    except URLError:        
        raise
    
    body = soup.find(attrs={"class":"cssboxwhite_body2","id":"data"})
    if not body:
        logger.info("url:"+url+" is NULL!!!!!!!!!!!!")
    else:
        names = body.contents[1].find("h4").getString().strip()
        co_index = names.find("(")
        real_name = names[0:co_index]
        co_name = names[co_index+1:-1]        
        co_name_array = co_name.split(u"、")        
        co_name_array.append(real_name)
        co_name = u"，".join(co_name_array)
        
        header = body.contents[1].find("img")        
        result = Actress.objects.get_or_create(name=real_name)        
        actress = result[0]
        logger.info("realname:"+str(actress.id)+">"+real_name+" coname:"+co_name)
        #create or update the actress
        actress.co_names = co_name
        if header is not None:
            link = header.get('src','')
            actress.photo = save_acttress_header(actress.id, link)
        else:
            logger.info("realname:"+str(actress.id)+">"+real_name+" no header photo!")
        dashrow = body.contents[1].find("ul",attrs={"class":"dashrow"})
        lis = dashrow.findAll('li')
        #logger.info("dashrow:"+dashrow.prettify())
        pf = []        
        for content in lis:
            text = content.getText().strip()
            if text != ":::":
                pf.append(text)    
            
        actress.profile = ";".join(pf)
        logger.info("profile:"+actress.profile)
        actress.save()
        return True
    
#把所有的演员资料下载本地   
def actresscron(request):    
    urlprefix = "http://avno1.com/?action-model-name-avgirls-itemid-"
    count = 0
    for n in range(400,480):
        url = urlprefix + str(n)
        if parseActress(url):
            count = count + 1
        time.sleep(1)   
    
    return render_to_response('btfactory/actresscount.html', locals())

def newfilm(request):
    movielist = MovieLink.objects.order_by('-id')
    paginator = Paginator(movielist, 10)
    try:
        page = request.GET.get('page')
        if page is None:
            result = paginator.page(1)
        else:    
            result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)    
    return render_to_response(u'btfactory/newfilm.html',{'film_list':result}, context_instance=RequestContext(request))
     
def daily(request):        
    parsed_daily_list = DailyLink.objects.order_by('-id')[:100]    
    result = []
    for daily in parsed_daily_list:
        movie_count = MovieLink.objects.filter(daily_link=daily).count()
        movie_confirm_count = MovieLink.objects.filter(daily_link=daily,parsed=True).count()
        image_loaded_count = MovieLink.objects.filter(daily_link=daily,images_loaded=True).count()
        result.append({'daily':daily,'count':movie_count,'confirmed':movie_confirm_count,'loaded':image_loaded_count})    
    return render_to_response(u'btfactory/daily.html',{'parsed_daily_list':result}, context_instance=RequestContext(request))

#电影和演员关联
def confirmMovie(request, movie_id):
    ml = get_object_or_404( MovieLink, pk=movie_id)
    
    #create relate actress
    ml.actress_names = request.POST['actress']
    actress_names = ml.actress_names.split(";")
    
    for actress in actress_names:        
        at = Actress.objects.get_or_create(name = actress)[0]
        at.save()
        ml.actress.add(at)  
        
    ml.parsed = True    
    ml.save()
    #refresh the daily movie link page
    return HttpResponseRedirect("/btfactory/"+str(ml.daily_link.id)+"/daily/")

def dailymovie(request, daily_id):        
    dl = get_object_or_404( DailyLink, pk=daily_id)
    movielinks = MovieLink.objects.filter(daily_link=dl).order_by('-id')[:100]    

    return render_to_response('btfactory/dailymovies.html', locals())

def actress(request):

    actress_list = Actress.objects.all().order_by('-update_date')[:5]

    return render_to_response('btfactory/index.html', locals())

def actressinfo(request, actress_id):

    #latest_movies_list = MovieLink.objects.all().order_by('-pub_date')[:5]
    actress = get_object_or_404(Actress, pk=actress_id)

    return render_to_response('btfactory/index.html', locals())
