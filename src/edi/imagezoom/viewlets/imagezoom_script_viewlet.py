# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from plone.app.layout.viewlets import ViewletBase
from plone import api as ploneapi

scaling = ['large', 'preview', 'mini', 'thumb', 'tile', 'icon', 'listing']

class ImagezoomScriptViewlet(ViewletBase):
    
    def update(self):
        self.manipulate = ""
        self.richimages = [] 
        htmltext = ''
        if self.context.portal_type == 'Skill':
            if self.context.bachelor:
                htmltext += self.context.bachelor.raw
        if hasattr(self.context, 'text'):
            if self.context.text:
                htmltext += self.context.text.raw
        soup = BeautifulSoup(htmltext, 'html.parser')
        textimages = soup.find_all('img', class_="image-richtext")
        for i in textimages:
            self.richimages.append(i)
            uid = i.get('data-val')
            imageobj = ploneapi.content.get(UID = uid)
            title = imageobj.title 
            index = textimages.index(i)
            self.manipulate += f'$("img.image-richtext")[{index}].setAttribute("data-val", "{uid}");'
            if not i.get('title'):
                self.manipulate += f'$("img.image-richtext")[{index}].setAttribute("title", "{title}");'
       
    def images(self):
        images = []
        for i in self.richimages:
            entry = dict()
            entry['title'] = i.get('title')
            entry['description'] = i.get('alt')
            uid = i.get('data-val')
            imageobj = ploneapi.content.get(UID = uid)
            if not entry['title']:
                entry['title'] = imageobj.title
            if not entry['description']:
                entry['description'] = imageobj.description
            imageurl = imageobj.absolute_url() + '/@@images/image'
            entry['id'] = "edi" + uid
            entry['src'] = imageurl
            images.append(entry)
        return images

    def zoom(self):
        zoommarker = False
        if hasattr(self.context, 'zoommarker'):
            zoommarker = self.context.zoommarker
        return zoommarker

    def render(self):
        return super(ImagezoomScriptViewlet, self).render()
