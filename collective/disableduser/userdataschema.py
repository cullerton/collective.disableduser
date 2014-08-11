# add extra fields to registration:
# http://pypi.python.org/pypi/collective.examples.userdata
from zope.interface import implements
from zope import schema

from collective.disableduser import appMessageFactory as _
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema


# This is referenced in profiles/default/componentregistry.xml
class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """
    disabled_user = schema.Bool(
        # title=_(u'label_disabled_user', default=u'Disabled User'),
        title=_(u'label_disabled_user', default=u'Disabled User'),
        description=_(
            u'help_disabled_user',
            default=u"Whether the user is disabled. False by default."),
        required=True,
        default=False,
    )
