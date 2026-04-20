from edi.imagezoom import _
from plone import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.interface import alsoProvides


class IImageZoomMarker(model.Schema):
    model.fieldset(
        "settings",
        label=_("Einstellungen"),
        fields=("zoommarker",),
    )

    zoommarker = schema.Bool(
        title="Bilder vergrößern aktivieren",
        default=False,
        required=False,
    )


alsoProvides(IImageZoomMarker, IFormFieldProvider)
