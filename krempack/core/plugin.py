#!/usr/bin/env python
## \file plugin.py
## \brief Plugin interface class and implementation of plugin handler
'''
# Copyright (C) 2017  Bitvis AS
#
# This file is part of KREM.
#
# KREM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# KREM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with KREM.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Bitvis AS 
# www.bitvis.no
# info@bitvis.no
'''
from collections import OrderedDict

from krempack.common import constants as c
from abc import ABCMeta, abstractmethod, abstractproperty
from importlib import import_module
import inspect

## Plugin interface 
#
# Generic plugin interface
class Plugin():
    __metaclass__ = ABCMeta
    
    ## Constructor
    #  : Must setup self.call_list={"<entrypoint>":<function>}
    def __init__(self):
        pass
    
    # Name of plugin
    @abstractproperty
    def name(self):
        pass
        
        
## Entrypoint class
#
# Contains execution information required for all entrypoints
class Entrypoint():

    ## Constructor
    # : Setup call list dictionary sections based on execution order
    # @param name : Name of entrypoint
    def __init__(self, name):
        self.name = name
        self.call_list=OrderedDict()
        self.call_list["first"]=[]
        self.call_list["dont_care"]=[]
        self.call_list["last"]=[]
        
    ##Call list section with 'random' execution order
    # @param function : Class Plugin
    def append_call_list(self, plugin):
        self.call_list["dont_care"].append(plugin)
        
    ##Call list section to execute first (First in, first out)
    # @param function : Class Plugin
    def append_first_to_execute(self, plugin):
        self.call_list["first"].append(plugin)
    
    ##Call list section to execute last (Last in, last out)
    # @param function : Class Plugin
    def append_last_to_execute(self, plugin):
        self.call_list["last"].append(plugin)
    
    ##Removes plugin function from entrypoint call list
    # @param function : Class Plugin
    def remove_from_call_list(self, plugin):
        for list in self.call_list:
            list = self.call_list[list]
            if plugin in list:                
                list.remove(plugin)
        
    ##'random' section of call list first contains all plugins using this entrypoint.
    #This function cleans up 'random' section after plugin functions have been added
    #to sections to execute last or first
    def synch_call_lists(self):
        plugins_to_remove=[]
        for plugin in self.call_list["dont_care"]:
            if plugin in self.call_list["first"] or plugin in self.call_list["last"]:
                plugins_to_remove.append(plugin)
                
        for plugin in plugins_to_remove:
            self.call_list["dont_care"].remove(plugin)
                
                
    ##Execute all plugin functions using this entrypoint in order
    #@param variables : Dict of variables passed to plugin function
    def execute(self, variables={}):
        all_ok = True
        for list in self.call_list:
            list = self.call_list[list]
            if len(list) > 0:
                for plugin in list:                    
                    try:
                        plugin = plugin()     
                        if hasattr(plugin, self.name):
                            plugin_function = getattr(plugin, self.name)
                            if variables is not None and len(variables) > 0:
                                plugin_function(**variables)
                            else:
                                plugin_function()
                    except Exception as e:
                        print('[ERROR]: In plugin: "' + str(plugin.name) + '" , entrypoint: "' + str(self.name) + '"')
                        print(str(e))
                        all_ok = False
                              
        return all_ok
        
## Plugin handler
#
# Register and execute plugins
class PluginHandler():
    entrypoints = OrderedDict()
    plugin_list = []
    
    ## Constructor
    #  : Initiates available entrypoints
    def __init__(self):
        for entrypoint in c.plugin_entry_points:
            self.entrypoints[entrypoint] = Entrypoint(entrypoint)
    
    ##Register new plugins
    # @param plugin : Class Plugin
    def register_plugin(self, plugin):
        all_ok = True
        if self.verify_plugin(plugin):
            self.plugin_list.append(plugin)

            for entrypoint in c.plugin_entry_points:
                if hasattr(plugin, entrypoint):
                    try:
                        self.entrypoints[entrypoint].append_call_list(plugin)
                    except Exception:
                        print('[ERROR]: Failed to register plugin: "' + str(plugin.name) + '", function for entrypoint: "' + str(entrypoint) + '"')
                        all_ok = False
                        self.unregister_plugin(plugin)
        else:
            all_ok = False
            
        return all_ok
            
    
    ##Unregister plugins
    # @param plugin : Class Plugin
    def unregister_plugin(self, plugin):
        all_ok = True

        for entrypoint in c.plugin_entry_points:
            if hasattr(plugin, entrypoiny):
                try:
                    self.entrypoints[entrypoint].remove_from_call_list(plugin)
                except Exception:
                    print('[ERROR]: Failed to unregister plugin: "' + str(plugin.name) + '", function for entrypoint: "' + str(entrypoint) + '"')
                    all_ok = False
        return all_ok
    
    ##Return instance of target plugin from list of registered plugins
    # @param plugin : Class Plugin
    def get_registered_plugin(self, plugin):
        plugin_found = None
        for registered_plugin in self.plugin_list:
            if plugin.name == registered_plugin.name:
                plugin_instance = registered_plugin
                
        if plugin_instance is None:
            print("[WARNING]: Failed to unregister plugin '" + plugin.name + "', as it was not registered")
            
        return plugin_instance
    
    ##Verify single plugin
    # @param plugin_instance : Class Plugin 
    def verify_plugin(self, plugin):
        plugin_ok = True
        
        # Check if already registered
        if plugin in self.plugin_list:
            print("[ERROR]: Attempted to register plugin '" + plugin.name + "', but it already exists")
            plugin_ok = False
        
        return plugin_ok

''' Test code
class TestPlugin(Plugin):
    name = "Test-plugin"
    call_list = {}
    
    def __init__(self):
        self.call_list["pre-job_execution"] = self.f_to_call
        
    def f_to_call(self, test):
        print("Variable passed: " + str(test))
        
class TestPlugin2(Plugin):
    name= "Test-plugin2"
    call_list={}
    
    def __init__(self):
        self.call_list["pre-job_execution"] = self.f_to_call
        
    def f_to_call(self, test):
        print("This is a test")

if __name__ == '__main__':
    plugin_handler = PluginHandler()
    
    plugin_handler.register_plugin(TestPlugin)
    plugin_handler.register_plugin(TestPlugin2)
    plugin_handler.unregister_plugin(TestPlugin)
    plugin_handler.entrypoints["pre-job_execution"].execute({"test":"This is a test"})
    '''
