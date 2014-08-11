from AccessControl.SecurityInfo import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins \
    import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IExtractionPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

from zExceptions import Redirect

import logging
logger = logging.getLogger("collective.disableduser: plugin:")

from collective.disableduser.disableduser import DisabledUser

manage_addDisabledUserPluginForm = \
    PageTemplateFile(
        '../www/addDisabledUser',
        globals(),
        __name__='manage_addDisabledUserPluginForm')


def addDisabledUserPlugin(self, id, title='', REQUEST=None):
    """Add Disabled User Plugin to Plone PAS"""
    obj = DisabledUserPlugin(id, title)
    self._setObject(obj.getId(), obj)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
            '%s/manage_main'
            '?manage_tabs_message=Disabled+User+PAS+Plugin+added.' %
            self.absolute_url())


class DisabledUserPlugin(BasePlugin):
    """Plugin for Disabled User"""

    meta_type = 'Disabled User'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    security.declarePrivate('extractCredentials')

    # IExtractionPlugin implementation
    def extractCredentials(self, request):
        """This is where our 'sts_receiver' code will end up"""
        # logger.info("STSPlugin: extractCredentials: ")
        redirect_url = "%s/disabled_user_redirect" % self.portal_url()

        # import pdb; pdb.set_trace()

        if 'form.submitted' in request.form:

            # logger.info(
            #     "STSPlugin: extractCredentials: request.form: %s" %
            #     str(request.form))
            __ac_name = request.form.get('__ac_name')
            # logger.info(
            #     "STSPlugin: extractCredentials: __ac_name: %s" %
            #     str(__ac_name))

            try:
                dtool = DisabledUser(self)
            except Exception, e:
                logger.info("extractCredentials: Exception: %s" % str(e))
                raise
            else:
                if __ac_name:
                    try:
                        is_disabled = dtool.is_disabled(__ac_name)
                    except Exception, e:
                        logger.info(
                            "extractCredentials: Exception: %s" % str(e))
                        raise
                    else:
                        logger.info(
                            "extractCredentials: is_disabled: %s" %
                            str(is_disabled))
                        if is_disabled:
                            raise Redirect(redirect_url)

        return None


classImplements(DisabledUserPlugin, IExtractionPlugin)
InitializeClass(DisabledUserPlugin)
