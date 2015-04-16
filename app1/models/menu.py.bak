# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('Incredible Varanasi'),XML('<sup> MADS</sup>'),
                  _class="brand",_href=URL('default','home'))
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Mehul Jain <mehul.jain.cse12@iitbhu.ac.in>'
response.meta.keywords = 'home'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'home'), []),
    (SPAN('About Us', _class='highlighted'), False, 'show',
     [(T('Contact'), False, URL('default', 'create'))]
    )
               ]

#if auth.has_membership('Managers'):
#    response.menu.append((T('Manage'),False,URL('default','manage')))
if "auth" in locals(): auth.wikimenu()
