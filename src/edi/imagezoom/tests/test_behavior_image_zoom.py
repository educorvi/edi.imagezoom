# -*- coding: utf-8 -*-
from edi.imagezoom.behaviors.image_zoom import IImageZoomMarker
from edi.imagezoom.testing import EDI_IMAGEZOOM_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class ImageZoomIntegrationTest(unittest.TestCase):

    layer = EDI_IMAGEZOOM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_behavior_image_zoom(self):
        behavior = getUtility(IBehavior, 'edi.imagezoom.image_zoom')
        self.assertEqual(
            behavior.marker,
            IImageZoomMarker,
        )
