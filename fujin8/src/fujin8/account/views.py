#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
基于django的新浪微博oauth views
需要django的session支持
"""
 
from django.http import HttpResponseRedirect
from weibopy.auth import OAuthHandler, WeibopError
from weibopy import oauth, User as SinaUser
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from account.models import UserProfile
from account.sinaweibo import sinaweibo

weibo_client = sinaweibo()

class WebOAuthHandler(OAuthHandler):
 
    def get_authorization_url_with_callback(self, callback, signin_with_twitter=False):
        #Get the authorization URL to redirect the user
        try:
            # get the request token
            self.request_token = self._get_request_token()
 
            # build auth request and return as url
            if signin_with_twitter:
                url = self._get_oauth_url('authenticate')
            else:
                url = self._get_oauth_url('authorize')
            request = oauth.OAuthRequest.from_token_and_callback(
                token=self.request_token, callback=callback, http_url=url
            )
            return request.to_url()
        except Exception, e:
            raise WeibopError(e)
 
 
def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/' # 避免外站直接跳到登录页而发生跳转错误
    return referer_url
 
def _oauth():
    #获取oauth认证类
    return WebOAuthHandler(weibo_client.consumer_key, weibo_client.consumer_secret)
 
def login(request):
    # 保存最初的登录url，以便认证成功后跳转回来
    back_to_url = _get_referer_url(request)
    request.session['login_back_to_url'] = back_to_url
 
    # 获取oauth认证url
    login_backurl = request.build_absolute_uri('/logincheck')
    auth_client = _oauth()
    auth_url = auth_client.get_authorization_url_with_callback(login_backurl)
    # 保存request_token，用户登录后需要使用它来获取access_token
    request.session['oauth_request_token'] = auth_client.request_token
    # 跳转到登录页面
    return HttpResponseRedirect(auth_url)
 
def login_check(request):
    """用户成功登录授权后，会回调此方法，获取access_token，完成授权"""
    # http://mk2.com/?oauth_token=c30fa6d693ae9c23dd0982dae6a1c5f9&oauth_verifier=603896
    verifier = request.GET.get('oauth_verifier', None)
    auth_client = _oauth()
    # 设置之前保存在session的request_token
    request_token = request.session['oauth_request_token']
    del request.session['oauth_request_token']
 
    auth_client.set_request_token(request_token.key, request_token.secret)
    access_token = auth_client.get_access_token(verifier)
    
    # 保存access_token，以后访问只需使用access_token即可                     
    weibo_client.setToken(access_token.key, access_token.secret)
    sinauser = weibo_client.get_myinfo() 
    username = "sinaweibo@"+str(sinauser.id) 
    password = u'temp'
    request.session['oauth_username'] = username
    request.session['oauth_access_token'] = access_token
    
    user = authenticate(username=username,password=password)
    if user is not None:
        if not user.is_active:                        
            # Return a 'disabled account' error message
            return HttpResponseRedirect('userdisenable')
    else:
        # 创建用户和用户资料数据
        user = User.objects.create_user(username,'',password)
        user.first_name = sinauser.id
        user.last_name = sinauser.screen_name
        user.save()
        userprofile = user.get_profile()
        userprofile.username = sinauser.name
        userprofile.save()
        user = authenticate(username=username,password=password)
 
    # 跳转回最初登录前的页面
    auth_login( request, user)
    back_to_url = request.session.get('login_back_to_url', '/')
    return HttpResponseRedirect(back_to_url)  
 
def logout(request):
    """用户登出，直接删除access_token"""    
    if(request.session.has_key('oauth_access_token')):
        del request.session['oauth_access_token']
    auth_logout(request);
    back_to_url = _get_referer_url(request)
    return HttpResponseRedirect(back_to_url)# Create your views here.


