# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import edi.imagezoom


class EdiImagezoomLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=edi.imagezoom)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'edi.imagezoom:default')


EDI_IMAGEZOOM_FIXTURE = EdiImagezoomLayer()


EDI_IMAGEZOOM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EDI_IMAGEZOOM_FIXTURE,),
    name='EdiImagezoomLayer:IntegrationTesting',
)


EDI_IMAGEZOOM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EDI_IMAGEZOOM_FIXTURE,),
    name='EdiImagezoomLayer:FunctionalTesting',
)


EDI_IMAGEZOOM_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        EDI_IMAGEZOOM_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='EdiImagezoomLayer:AcceptanceTesting',
)
