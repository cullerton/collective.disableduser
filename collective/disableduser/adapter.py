# add extra fields to registration:
# http://pypi.python.org/pypi/collective.examples.userdata
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_disabled_user(self):
        return self.context.getProperty('disabled_user', '')

    def set_disabled_user(self, value):
        return self.context.setMemberProperties({'disabled_user': value})

    disabled_user = property(get_disabled_user, set_disabled_user)
