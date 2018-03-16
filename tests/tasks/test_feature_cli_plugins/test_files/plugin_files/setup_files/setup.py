from krempack.core import plugin

'''
Use following import if krem_plugins repo is placed in library,
or add other plugins in the same way
'''
from library.plugins import test_plugins

'''
to get krem_plugins: 
cd <krem project>/library/plugins
git clone https://github.com/Bitvis/krem_plugins.git
'''

def setup_plugins(plugin_handler):
    # Register runtime plugins here
    '''
    Uncomment the following to enable some of the plugins from krem_plugins,
    or add other plugins in the same way
    '''
    #plugin_handler.register_plugin(PluginPrintTaskResults)

    pass

def setup_cli_plugins(plugin_handler):
    # Register CLI plugins here
    '''
    Uncomment the following to enable some of the plugins from krem_plugins,
    or add other plugins in the same way
    '''
    plugin_handler.register_plugin(test_plugins.TestPluginCliHooks)

    pass

