# -*- coding: utf-8 -*-

# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import RequestContext
from douban import doubanUtil
import json
import urllib2
import urllib
import os
from cookielib import CookieJar
from django.views.decorators.csrf import csrf_exempt
import time
import pickle

#globals()

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


def initopener():
    header = (
        'User-Agent',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.76 Safari/537.36'
    )
    privatecookiejar = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(privatecookiejar))
    opener.addheaders = [header]
    return opener

# 应该是正确应用django csrf的例子了吧
def login_user(request):
    if request.method == 'POST':
        opener = doubanUtil.initopener()
        captchaid = request.session['captchaid']

        print captchaid

        request.session.clear()

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        captcha = request.POST.get('captcha', '')

        print 'username=>' + str(username)
        print 'password=>' + str(password)
        print 'captcha=>' + str(captcha)

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
            playlist = doubanUtil.play(channel=-3, opener=opener)
            picklePath = os.path.join(os.path.dirname(__file__), '..', 'picklefile').replace('\\', '/')
            with open(str(picklePath) + '/playlist.pickle', 'wb') as listSaveData:
                pickle.dump(playlist, listSaveData)


        #time.sleep(300)

        return HttpResponseRedirect('/douban/index/')
        #return HttpResponseRedirect('/auth/test/')

    else:
        opener = doubanUtil.initopener()
        captchaid = doubanUtil.getcaptcha(opener)
        request.session['captchaid'] = captchaid

        print captchaid

        return render_to_response('new_auth_login.html', {}, context_instance=RequestContext(request))

#def playmusic(request):


def test(request):
    picklePath = os.path.join(os.path.dirname(__file__), '..', 'picklefile').replace('\\', '/')
    with open(str(picklePath) + '/playlist.pickle', 'rb') as listSaveData:
        playlist = pickle.load(listSaveData)

    print type(playlist)
    print playlist
    songlist = json.dumps(playlist)
    print type(songlist)
    print songlist
    #return HttpResponse('hello cleantha')
    #print request.GET['getsong']
    return HttpResponse(songlist, mimetype='application/json')


#下面这样写 把opener放在全局变量中传值 会出现联系两次提交表单 第二次提交之后django 返回HTTP Error 403: Forbidden django错误
'''
param = []
def login_user(request):
    if request.method == 'POST':
        captchaid = param[0]
        opener = param[1]

        print captchaid

        request.session.clear()

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        captcha = request.POST.get('captcha', '')

        print 'username=>' + str(username)
        print 'password=>' + str(password)
        print 'captcha=>' + str(captcha)

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
            #return opener
            doubanUtil.play(channel=-3, opener=opener)

        return HttpResponseRedirect('/douban/index/')

    else:
        opener = doubanUtil.initopener()
        captchaid = doubanUtil.getcaptcha(opener)
        param.append(captchaid)
        param.append(opener)

        print captchaid

        return render_to_response('auth_login.html', {}, context_instance=RequestContext(request))
'''
