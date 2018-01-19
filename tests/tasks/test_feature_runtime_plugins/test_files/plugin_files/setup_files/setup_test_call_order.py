

from krempack.core import plugin
from library.plugins import test_plugins

def setup_plugins(plugin_handler):
    plugin_handler.register_plugin(test_plugins.PluginCalledThird)
    plugin_handler.register_plugin(test_plugins.PluginCalledFirst)
    plugin_handler.register_plugin(test_plugins.PluginCalledSecond)
    plugin_handler.register_plugin(test_plugins.PluginCheckCallOrder)

    plugin_handler.entrypoints["job_start"].append_first_to_execute(test_plugins.PluginCalledFirst)
    plugin_handler.entrypoints["job_start"].append_first_to_execute(test_plugins.PluginCalledSecond)
    plugin_handler.entrypoints["job_start"].append_last_to_execute(test_plugins.PluginCalledThird)
