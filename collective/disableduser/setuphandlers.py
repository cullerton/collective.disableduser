from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
from collective.disableduser.plugin import addDisabledUserPlugin

def importVarious(context):
    ''' Install the Disabled User plugin
    '''
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('collective-disableduser.txt') is None:
        return

    out = StringIO()
    portal = context.getSite()

    uf = getToolByName(portal, 'acl_users')
    installed = uf.objectIds()

    if 'disableduserpas' not in installed:
        addDisabledUserPlugin(uf, 'disableduserpas', 'Disabled User PAS')
        activatePluginInterfaces(portal, 'disableduserpas', out)
    else:
        print >> out, 'disableduserpas already installed'

    print out.getvalue()
