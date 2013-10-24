# -*- coding: utf-8 -*-
import urllib
import urllib2
from cookielib import CookieJar
import sys
import json
import os


def getcaptcha(opener):
    captchaid = opener.open(urllib2.Request('http://douban.fm/j/new_captcha')).read().strip('"')
    getcaptchaimg(opener, captchaid)
    return captchaid


def getcaptchaimg(opener, captchaid):
    captcha = opener.open(urllib2.Request('http://douban.fm/misc/captcha?size=m&id=' + str(captchaid))).read()
    # wb means write binary data
    captchaPath = os.path.join(os.path.dirname(__file__), '..', 'captchafile').replace('\\', '/')
    captchafile = open(str(captchaPath) + '/captcha.jpg', 'wb')
    captchafile.write(captcha)
    captchafile.close()


class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        super.http_error_302(fp, code, msg, headers)
        print 'req===>' + str(req)
        print 'headers===>' + str(headers)


def initopener():
    header = (
        'User-Agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
    )
    host = ('Host',
             'douban.fm'
    )
    refer = ('Referer',
             'http://douban.fm/'
    )
    connect = ('Connection',
               'keep-alive'
    )

    #proxy_support = urllib2.ProxyHandler({'http': 'http://127.0.0.1:8087'})
    privatecookiejar = CookieJar()
    httphandler = urllib2.HTTPHandler(debuglevel=1)
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(privatecookiejar), httphandler)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(privatecookiejar))
    opener.addheaders = [header, host, refer, connect]
    return opener


def doubanfmlogin(username='zjhsdtc@sohu.com', password='z1x2c3v41598753', captcha='cleantha', captchaid=33,
                  opener=None):
    print captcha
    print captchaid
    while True:
        jsonResponse = json.loads(opener.open(urllib2.Request('http://douban.fm/j/login', urllib.urlencode({
            'source': 'radio',
            'alias': username,
            'form_password': password,
            'captcha_solution': captcha,
            'captcha_id': captchaid,
            'task': 'sync_channel_list'
        }))).read())

        if 'err_msg' in jsonResponse.keys():
            print jsonResponse['err_msg']
        else:
            print 'login successful!!!'
            return opener


def getPlayList(channel='0', opener=None):
    #url = 'http://douban.fm/j/mine/playlist?type=n&channel=%s' % channel
    url = 'http://douban.fm/j/mine/playlist?type=n&sid=&pt=0.0&channel=%s&from=mainsite&r=f5b061dff2' % channel
    print url
    #匿名登陆
    if opener == None:
        return json.loads(urllib2.urlopen(url).read())
    else:
        return json.loads(opener.open(urllib2.Request(url)).read())


def play(channel='0', opener=None):
    if opener == None:
        playlist = getPlayList(channel=channel)
    else:
        playlist = getPlayList(channel=channel, opener=opener)

    if playlist['song'] == []:
        print 'get songlist failed'
    else:
        songlist = []
        for song in playlist['song']:
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

        return songlist

        #picturename = playlist['song'][0]['picture'].split('/')[-1]
        #songname = playlist['song'][0]['url'].split('/')[-1]
        #print 'total songs => ' + str(len(playlist['song']))
        #print playlist['song'][0]['picture']
        #print playlist['song'][0]['url']
        #if opener != None:
        #    getsongimg(openner=opener, imgurl=playlist['song'][0]['picture'], songname=picturename)
        #    downloadsong(songname=songname, url=playlist['song'][0]['url'])

        #player = subprocess.Popen(['/Applications/MPlayerX.app/Contents/MacOS/MPlayerX', playlist['song'][0]['url']])
        #time.sleep(playlist['song'][0]['length'])
        #player.kill()

import requests

from django.http import HttpResponseRedirect

def getcaptcha8(email, password):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; zh-CN) AppleWebKit/533.3 (KHTML, like Gecko) radio Safari/533.3'
    }

    params = {
        'email': email,
        'password': password,
        'app_name': 'radio_desktop_win',
        'version': '100'
    }

    r = requests.post('http://www.douban.com/j/app/login', data=params, headers=headers)
    # print dict(r.text)
    # print type(r.text)
    result = json.loads(r.text)
    print type(result)

    try :
        user_id = result['user_id']
        expire = result['expire']
        token = result['token']
        print user_id
        print expire
        print token
        channel = '-3'
    except:
        print 'result======>' + str(result['err'])

    url = 'http://www.douban.com/j/app/radio/people?app_name=radio_desktop_win&version=100&user_id=%s&expire=%s&token=%s&sid=&h=&channel=%s&type=n' % (user_id, expire, token, channel)
    newr = requests.get(url, headers=headers)
    newresponse = json.loads(newr.text)
    print type(newresponse)
    #print newresponse['song']
    if newresponse['song'] == []:
        print 'get songlist failed'
    else:
        songlist = []
        for song in newresponse['song']:
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

        return songlist



