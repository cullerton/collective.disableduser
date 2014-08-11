from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from interfaces import IDisabledUser
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DisabledUserRedirect(BrowserView):
    """Simple redirect page for disabled user attempted logins"""

    template = ViewPageTemplateFile('www/disabled_user_redirect.pt')

    def __call__(self):
        """"""
        return self.template()


class DisabledUser(BrowserView):
    """Set disable and enable user attribute"""

    implements(IDisabledUser)

    def __init__(self, context):
        self.context = context

    def disable_user(self, userid=None):
        """disable user by setting disabled_user property to True"""
        pt = getToolByName(self.context, 'portal_membership')
        member = pt.getMemberById(userid)
        user = member.getUser()
        user.setProperties(disabled_user=True)

    def enable_user(self, userid=None):
        """enable user by setting disabled_user property to False"""
        pt = getToolByName(self.context, 'portal_membership')
        member = pt.getMemberById(userid)
        user = member.getUser()
        user.setProperties(disabled_user=False)

    def is_disabled(self, userid=None):
        """test if user is disabled by querying disabled_user property"""
        pt = getToolByName(self.context, 'portal_membership')
        member = pt.getMemberById(userid)
        user = member.getUser()
        is_disabled = user.getProperty("disabled_user")
        is_disabled = False if is_disabled is None else is_disabled

        return is_disabled
