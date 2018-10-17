#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
import logging
from google.appengine.ext import ndb


###Jinja2の設定
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


###Datastoreの設定クラス
class UserData(ndb.Model):
    name = ndb.StringProperty()
    age = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)


###テンプレHTMLハンドラの設定クラスbase
class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))


###Baseハンドラを継承し、main.htmlを表示する
class MainHandler(BaseHandler):
    def get(self):
        users = UserData.query().order(-UserData.date).fetch(10)
        values = {
            'users':users
        }
        self.render('/templates/main.html', values)

    def post(self):
        name = self.request.get('name')
        age_str = self.request.get('age')
        if name is None or age_str is None:
            self.redirect('/')
        #age入力が文字列だった場合の例外処理
        try:
            int(age_str)
        except ValueError:
            self.redirect('/')
            return
        user = UserData()
        user.name = name
        user.age = int(age_str)
        user.put()
        self.redirect('/')

class SayHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("============= /say ==============")
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/say', SayHandler),
], debug=True)