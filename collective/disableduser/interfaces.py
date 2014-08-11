from zope.interface import Interface


class IDisabledUser(Interface):
    """Marker interface for collective.disableduser product layer"""

    def enable_user(self, userid):
        pass

    def disable_user(self, userid):
        pass
