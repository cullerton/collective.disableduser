from Products.PluggableAuthService.PluggableAuthService \
    import registerMultiPlugin
from collective.disableduser import plugin
from zope.i18nmessageid import MessageFactory

appMessageFactory = MessageFactory('codec.app')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    registerMultiPlugin(plugin.DisabledUserPlugin.meta_type)  # Add to PAS menu
    context.registerClass(plugin.DisabledUserPlugin,
                          constructors=(plugin.manage_addDisabledUserPluginForm,
                          plugin.addDisabledUserPlugin),
                          visibility=None)
