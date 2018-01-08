#!/usr/bin/env python

from krempack.core import plugin
from library.plugins import test_plugins

def setup_plugins(plugin_handler):
    plugin_handler.register_plugin(test_plugins.TestPluginAllEntrypoints)
