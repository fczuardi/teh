#!/usr/bin/env python
# encoding: utf-8
"""
webapp.py

Created by Pradeep Gowda on 2008-04-23.
Copyright (c) 2008 Yashotech. All rights reserved.
"""
import wsgiref.handlers

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import users

import os
from teh.lib import utils, markdown2, BeautifulSoup
from teh.utils import TehRequestHandler, administrator, TehConfig
import teh.blog
import teh.admin


class LoginHandler(TehRequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            self.redirect('./')

class LogoutHandler(TehRequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.redirect(users.create_logout_url('./'))
        else:
            self.redirect('./')

class HomePageHandler(TehRequestHandler):
    def get(self):
        entries = teh.blog.Entry.all()
        entries.filter("static =", False)
        entries.order('-published').fetch(limit=5)
        self.render("templates/home.html", entries=entries)

        
def main():
    application = webapp.WSGIApplication([
        (r"/teh/", HomePageHandler),
        (r"/teh/login", LoginHandler),
        (r"/teh/logout", LogoutHandler),

        (r"/teh/entries", teh.blog.EntryIndexHandler),
        (r"/teh/feed", teh.blog.FeedHandler),
        (r"/teh/entry/([^/]+)", teh.blog.EntryHandler),
        (r"/teh/entry/([^/]+)/edit", teh.blog.NewEntryHandler),
        (r"/teh/entry/([^/]+)/del", teh.blog.EntryDeleteHandler),
        (r"/teh/([^/]+)/edit", teh.blog.NewEntryHandler),
        (r"/teh/([^/]+)/del", teh.blog.EntryDeleteHandler),
        (r"/teh/topic/([^/]+)", teh.blog.TagHandler),
        
        (r"/teh/admin", teh.admin.AdminHandler),
        (r"/teh/admin/new", teh.blog.NewEntryHandler),
        (r"/teh/admin/config", teh.admin.ConfigHandler),
        (r"/teh/admin/entrylist", teh.admin.EntryListHandler),

       # (r"/shooin/([^/]+)", shooin.ShooinHandler),
        (r"/teh/([^/]+)", teh.blog.PageHandler),
        ], debug=True)
    
    config = TehConfig.all()
    if config.count() > 0:
        config = config.fetch(1)[0]
    else: 
        config1 = TehConfig(title="TEH Blog")
        config1.put()
       
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
    main()
