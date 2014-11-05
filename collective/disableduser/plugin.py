from AccessControl.SecurityInfo import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.interfaces.plugins \
    import IExtractionPlugin
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements

from zExceptions import Redirect

import logging
logger = logging.getLogger("collective.disableduser: plugin:")

from collective.disableduser.disableduser import DisabledUser

from Products.statusmessages.interfaces import IStatusMessage

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

    # stole this from betahaus.emaillogin which was messing with me
    def _get_username_from_email(self, login_email, get_all=False):
        """Returns the username for a given email.
           If no user found it returns None"""

        emails = []
        pas = self._getPAS()
        mail_props = self.getProperty('mail_props', ('email',))
        for mail_key in mail_props:
            query = {mail_key: login_email, "exact_match": True}
            for user in pas.searchUsers(**query):
                if not get_all:
                    return user['login']
                emails.append(user['login'])
        return emails
        # return None

    security.declarePrivate('extractCredentials')

    def extractCredentials(self, request):
        """This is where our 'sts_receiver' code will end up"""
        # logger.info("DisabledUserPlugin: extractCredentials: ")
        redirect_url = "%s/disabled_user_redirect" % self.portal_url()
        redirect_message = u'Login failed. ' + \
            'Both login name and password are case sensitive. ' + \
            'Check that caps lock is not enabled.'

        if 'form.submitted' in request.form:

            # logger.info(
            #     "DisabledUserPlugin: extractCredentials: request.form: %s" %
            #     str(request.form))
            __ac_name = request.form.get('__ac_name')
            logger.info(
                "DisabledUserPlugin: extractCredentials: __ac_name: %s" %
                str(__ac_name))
            if '@' in __ac_name:
                __ac_name = self._get_username_from_email(__ac_name)
            logger.info(
                "DisabledUserPlugin: extractCredentials: __ac_name: %s" %
                str(__ac_name))

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
                            messages = IStatusMessage(request)
                            messages.add(redirect_message, type=u"error")
                            raise Redirect(redirect_url)

        return None


classImplements(DisabledUserPlugin, IExtractionPlugin)
InitializeClass(DisabledUserPlugin)
