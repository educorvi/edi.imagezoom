# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from plone.app.layout.viewlets import ViewletBase

scaling = ['large', 'preview', 'mini', 'thumb', 'tile', 'icon', 'listing']

def extract_image_id(url):
    # Parse the URL and split the path
    path_parts = urlparse(url).path.strip("/").split("/")
    # Return the last part before the file extension
    if path_parts:
        last_part = path_parts[-1]
        return last_part.split(".")[0]  # Remove extension if present
    return None

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
            if i.get('data-val'):
                entry['id'] = "edi" + i.get('data-val')
            else:
                entry['id'] = "edi" + extract_image_id(i.get('src'))
            src = i.get('src')
            spliturl = src.split('/')
            if spliturl[-1] in scaling:
                url = "/".join(spliturl[:-1])
            else:
                url = src
            entry['src'] = url
            entry['orig'] = url.replace('@@images', '@@download/image')
            images.append(entry)
        return images

    def zoom(self):
        zoommarker = False
        if hasattr(self.context, 'zoommarker'):
            zoommarker = self.context.zoommarker
        return zoommarker

    def render(self):
        return super(ImagezoomScriptViewlet, self).render()
