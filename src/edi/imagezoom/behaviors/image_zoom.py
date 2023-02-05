# -*- coding: utf-8 -*-

from edi.imagezoom import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.supermodel import model
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from zope.interface import provider
from zope.interface import alsoProvides
from plone.autoform.interfaces import IFormFieldProvider


class IImageZoomMarker(model.Schema):

    model.fieldset(
            'settings',
            label=_(u'Einstellungen'),
            fields=('zoommarker',),
        )

    zoommarker = schema.Bool(
        title=u"Bilder vergrößern aktivieren",
        default=False,
        required=False,
        )

alsoProvides(IImageZoomMarker,IFormFieldProvider)    
