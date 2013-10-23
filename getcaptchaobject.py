# -*- coding: utf-8 -*-
import urllib
import urllib2
from cookielib import CookieJar
# 子进程模块
import subprocess
# 获得命令行参数
import sys
import os
# 解析命令行参数
import getopt
import time
import json
# 提示在命令行下输入密码
import getpass
import ConfigParser

#'openExpPan=Y; flag="ok"; ac="1382190201"; bid="L+y5ERIXBEY"; __utma=58778424.1146859312.1372921010.1382514904.1382517517.71; __utmb=58778424.5.9.1382517558232; __utmc=58778424; __utmz=58778424.1382439292.69.49.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=58778424.4482'

class HttpRedirect_Handler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print 'clea!!!!!!!!!!!!!!!!!!!!!!!!'
        #print GetCaptchaObj.captchacookiejar._cookies.values()
        #print GetCaptchaObj.captchacookiejar
        #print fp
        #print headers['Location']
        #print headers['Set-Cookie']
        print headers['Location']
        print 'hello!!!!!!!!!!!!!!!!!!!!!!!'


class GetCaptchaObj():
    captchacookiejar = CookieJar()

    def __init__(self):
        print 'init!!!'

    def initopener(self):
        header = (
            'User-Agent',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
        )
        #cookie = (
        #    'Cookie',
        #    'openExpPan=Y; flag="ok"; ac="1382190201"; bid="L+y5ERIXBEY"; __utma=58778424.1146859312.1372921010.1382514904.1382517517.71; __utmb=58778424.5.9.1382517558232; __utmc=58778424; __utmz=58778424.1382439292.69.49.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=58778424.4482'
        #)
        cookie = (
            'Cookie',
            'bid="KC5/Ag9G7eA"; path=/; domain=.douban.com; expires=Thu, 23-Oct-2014 10:24:28 GMT, flag="ok"; path=/; domain=.douban.fm'
        )


        host = ('Host',
                'douban.fm'
        )

        connect = ('Connection',
                   'keep-alive'
        )


        httphandler = urllib2.HTTPHandler(debuglevel=1)
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(privatecookiejar), httphandler)

        opener = urllib2.build_opener(HttpRedirect_Handler(), urllib2.HTTPCookieProcessor(GetCaptchaObj.captchacookiejar))
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(GetCaptchaObj.captchacookiejar))
        opener.addheaders = [header, cookie, connect, host]

        #captchaid = opener.open(urllib2.Request('http://douban.fm/j/new_captcha')).read().strip('"')
        captchaid = opener.open(urllib2.Request('http://douban.fm_captcha?&sig=e356116eac&response_nonce=1382524290&data=%B1%B7%8D%DE%7BZ.Y%23%1EqjwnX%E1%84%D4Vz%8C%9B%85g+%C3%C6%5D%FED9%96%84%D4Vz%8C%9B%85g+%C3%C6%5D%FED9%96%84%D4Vz%8C%9B%85g+%C3%C6%5D%FED9%96&mode=setup_needed&return_to=http%3A%2F%2Fdouban.fm_captcha%3F')).read().strip('"')

        print captchaid


if __name__ == '__main__':
    GetCaptchaObj().initopener()