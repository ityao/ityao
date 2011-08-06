#coding:utf-8
'''
Created on 2011-8-5

@author: silver
'''
from weibopy.auth import OAuthHandler
from weibopy.api import API


class sinaweibo(object):
    
    # 设置你申请的appkey
    consumer_key = '3548424667' 
    #设置你申请的appkey对于的secret
    consumer_secret = '5842a9cd9d2706dacd8ba679a2529164'
    
    def __init__(self):
        self.consumer_key = self.consumer_key
        self.consumer_secret = self.consumer_secret
     
    def getAtt(self, key):
        try:
            return self.obj.__getattribute__(key)
        except Exception, e:
            print e
            return ''
         
    def getAttValue(self, obj, key):
        try:
            return obj.__getattribute__(key)
        except Exception, e:
            print e
            return ''
         
    def auth(self):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth_url = self.auth.get_authorization_url()
        print 'Please authorize: ' + auth_url
        verifier = raw_input('PIN: ').strip()
        self.auth.get_access_token(verifier)
        self.api = API(self.auth)
      
    def setToken(self, token, tokenSecret):
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.setToken(token, tokenSecret)
        self.api = API(self.auth)
     
    def update(self, message):
        message = message.encode("utf-8")
        status = self.api.update_status(status=message)
        self.obj = status
        id = self.getAtt("id")        
        return id
         
    def destroy_status(self, id):
        status = self.api.destroy_status(id)
        self.obj = status
        id = self.getAtt("id")        
        return id
     
    def comment(self, id, message):
        comment = self.api.comment(id=id, comment=message)
        self.obj = comment
        mid = self.getAtt("id")
        return mid
     
    def comment_destroy (self, mid):
        comment = self.api.comment_destroy(mid)
        self.obj = comment
        mid = self.getAtt("id")
        text = self.getAtt("text")
        return mid
     
    def repost(self, id, message):
        post = self.api.repost(id=id, status=message)
        self.obj = post
        mid = self.getAtt("id")
        return mid
     
    def get_username(self):
        if getattr(self, '_username', None) is None:
            self._username = self.auth.get_username()
        return self._username
    
    def get_myinfo(self):
        self.obj = self.api.me()
        return self.obj
