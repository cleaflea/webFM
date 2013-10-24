# -*- coding: utf-8 -*-
import urllib
import urllib2
from cookielib import CookieJar
import sys
import json
import os
import requests
from django.http import HttpResponse
import pickle

class Douban():
    def __init__(self):
        self.email = ''
        self.password = ''
        # 伪造windows客户端的请求
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533.3 (KHTML, like Gecko) radio Safari/533.3'
        }
        self.app_name = 'radio_desktop_win'
        self.version = '100'
        self.loginurl = 'http://www.douban.com/j/app/login'
        self.getSongBaseUrl = 'http://www.douban.com/j/app/radio/people?app_name=radio_desktop_win&version=100&user_id=%s&expire=%s&token=%s&sid=&h=&channel=%s&type=n'
        self.getSongUrl = ''

        self.user_id = ''
        self.expire = ''
        self.token = ''
        self.token = ''
        self.channel = ''


    def login(self, email, password, channel):
        self.email = email
        self.password = password
        self.channel = channel

        loginparams = {
            'email': self.email,
            'password': self.password,
            'app_name': self.app_name,
            'version': self.version
        }

        loginrequest = requests.post(self.loginurl, data=loginparams, headers=self.headers)
        loginresult = json.loads(loginrequest.text)

        try:
            self.user_id = loginresult['user_id']
            self.expire = loginresult['expire']
            self.token = loginresult['token']

            self.getSong()

            return 'success'
        except:
            errormsg = loginresult['err']
            return errormsg

    def getSong(self):
        self.getSongUrl = self.getSongBaseUrl % (self.user_id, self.expire, self.token, self.channel)
        getSongRequest = requests.get(self.getSongUrl, headers=self.headers)
        getSongResult = json.loads(getSongRequest.text)

        if getSongResult['song'] == []:
            picklePath = os.path.join(os.path.dirname(__file__), '..', 'picklefile').replace('\\', '/')
            with open(str(picklePath) + '/playlist.pickle', 'wb') as listSaveData:
                pickle.dump('get songlist failed', listSaveData)

        else:
            songlist = []
            for song in getSongResult['song']:
                songlist.append(
                    {
                        'title': song['title'],
                        'artist': song['artist'],
                        'album': song['albumtitle'],
                        'cover': song['picture'],
                        'mp3': song['url'],
                        'ogg': song['url']
                    }
                )

            picklePath = os.path.join(os.path.dirname(__file__), '..', 'picklefile').replace('\\', '/')
            with open(str(picklePath) + '/playlist.pickle', 'wb') as listSaveData:
                pickle.dump(songlist, listSaveData)

