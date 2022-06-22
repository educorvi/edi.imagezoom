# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from plone.app.layout.viewlets import ViewletBase

scaling = ['large', 'preview', 'mini', 'thumb', 'tile', 'icon', 'listing']

class ImagezoomScriptViewlet(ViewletBase):

    def images(self):
        images = []
        if not self.zoom():
            return images
        htmltext = ''
        if self.context.portal_type == 'Skill':
            if self.context.bachelor:
                htmltext += self.context.bachelor.output
        if hasattr(self.context, 'text'):
            if self.context.text:
                htmltext += self.context.text.output
        soup = BeautifulSoup(htmltext, 'html.parser')
        textimages = soup.find_all('img')
        for i in textimages:
            entry = dict()
            entry['title'] = i.get('title')
            entry['description'] = i.get('alt')
            entry['id'] = "edi" + i.get('data-val')
            src = i.get('src')
            spliturl = src.split('/')
            if spliturl[-1] in scaling:
                url = "/".join(spliturl[:-1])
            else:
                url = src
            entry['src'] = url
            images.append(entry)
        return images

    def zoom(self):
        zoommarker = False
        if hasattr(self.context, 'zoommarker'):
            zoommarker = self.context.zoommarker
        return zoommarker

    def render(self):
        return super(ImagezoomScriptViewlet, self).render()
