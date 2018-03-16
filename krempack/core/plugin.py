
## \file plugin.py
## \brief Plugin interface class and implementation of plugin handler
'''
# Copyright (C) 2018  Bitvis AS
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
    #  : Must setup self.call_list={"<hook>":<function>}
    def __init__(self):
        pass
    
    # Name of plugin
    @abstractproperty
    def name(self):
        pass
        
        
## Hook class
#
# Contains execution information required for all hooks
class Hook():

    ## Constructor
    # : Setup call list dictionary sections based on execution order
    # @param name : Name of hook
    def __init__(self, name):
        self.name = name
        self.call_list=OrderedDict()
        self.call_list["first"]=[]
        self.call_list["dont_care"]=[]
        self.call_list["last"]=[]
        self.logger = None
        
    ##Call list section with 'random' execution order
    # @param function : Class Plugin
    def append_call_list(self, plugin):
        self.call_list["dont_care"].append(plugin.name)
        
    ##Call list section to execute first (First in, first out)
    # @param function : Class Plugin
    def append_first_to_execute(self, plugin):
        self.call_list["first"].append(plugin.name)
    
    ##Call list section to execute last (Last in, last out)
    # @param function : Class Plugin
    def append_last_to_execute(self, plugin):
        self.call_list["last"].append(plugin.name)
    
    ##Removes plugin function from hook call list
    # @param function : Class Plugin
    def remove_from_call_list(self, plugin):
        for list in self.call_list:
            list = self.call_list[list]
            if plugin in list:                
                list.remove(plugin.name)
        
    ##'random' section of call list first contains all plugins using this hook.
    #This function cleans up 'random' section after plugin functions have been added
    #to sections to execute last or first
    def synch_call_lists(self):
        plugins_to_remove=[]
        for plugin in self.call_list["dont_care"]:
            if plugin in self.call_list["first"] or plugin in self.call_list["last"]:
                plugins_to_remove.append(plugin)
                
        for plugin in plugins_to_remove:
            self.call_list["dont_care"].remove(plugin) 
                
    ##Execute all plugin functions using this hook in order
    #@param arguments : Dict of arguments passed to plugin function
    def execute(self, plugin_instances, arguments={}):
        error = False
        for list in self.call_list:
            list = self.call_list[list]
            if len(list) > 0:
                for plugin in list:                    
                    try:  
                        plugin = plugin_instances[plugin]
                        if hasattr(plugin, self.name):
                            plugin_function = getattr(plugin, self.name)
                            ret = None
                            if arguments is not None and len(arguments) > 0:
                                ret = plugin_function(**arguments)
                            else:
                                ret = plugin_function()
                            if ret:
                                error = True
                                break
                    except Exception as e:
                        self.log('In plugin: "' + str(plugin.name) + '" , hook: "' + str(self.name) + '"', 'error')
                        self.log(str(e), 'error')
                        error = True
                        break
              
        return error
    
    def set_logger(self, logger):
        self.logger = logger

    def get_logger(self):
        return self.logger

    def log(self, text, level):
        if self.logger is not None:
            self.logger.write(text, level)
        else:
            if level == 'warn':
                text = "[WARNING]: " + text
            if level == 'error':
                text = "[ERROR]: " + text
            print(text)


## Plugin handler
#
# Register and execute plugins
class PluginHandler():
    
    ## Constructor
    #  : Initiates available hooks
    def __init__(self, type):
        self.hooks = OrderedDict()
        self.plugin_instances = OrderedDict()
        self.hook_names = []
        self.logger = None

        if type == "runtime":
            self.hook_names = c.runtime_hooks
            for hook in c.runtime_hooks:
                self.hooks[hook] = Hook(hook)

        elif type == "cli":
            self.hook_names = c.cli_hooks
            for hook in c.cli_hooks:
                self.hooks[hook] = Hook(hook)
    
    ##Register new plugins
    # @param plugin : Class Plugin
    def register_plugin(self, plugin):
        plugin = plugin()
        all_ok = True
        if self.verify_plugin(plugin):
            self.plugin_instances[plugin.name] = plugin

            for hook in self.hook_names:
                if hasattr(plugin, hook):
                    try:
                        self.hooks[hook].append_call_list(plugin)
                    except Exception:
                        self.log('Failed to register plugin: "' + str(plugin.name) + '", function for hook: "' + str(hook) + '"', 'error')
                        all_ok = False
                        self.unregister_plugin(plugin)
        else:
            all_ok = False
            
        return all_ok
            
    def execute_hook(self, hook_name, arguments):
        error = False
        if hook_name in self.hooks:
            error = self.hooks[hook_name].execute(self.plugin_instances, arguments)
        else:
            self.log("Hook '" + hook_name + "' does not exist", 'error')
            error = True
        return error
    
    ##Unregister plugins
    # @param plugin : Class Plugin
    def unregister_plugin(self, plugin):
        all_ok = True

        for hook in self.hook_names:
            if hasattr(plugin, hook):
                try:
                    self.hooks[hook].remove_from_call_list(plugin)
                except Exception:
                    self.log('Failed to unregister plugin: "' + str(plugin.name) + '", function for hook: "' + str(hook) + '"', 'error')
                    all_ok = False
        return all_ok
    
    ##Return instance of target plugin from list of registered plugins
    # @param plugin : Class Plugin
    def get_registered_plugin(self, plugin):
        plugin_instance = None
        for registered_plugin in self.plugin_instances:
            if plugin.name == registered_plugin.name:
                plugin_instance = registered_plugin
                
        if plugin_instance is None:
            self.log("Failed to unregister plugin '" + plugin.name + "', as it was not registered", 'warn')
            
        return plugin_instance
    
    ##Verify single plugin
    # @param plugin_instance : Class Plugin 
    def verify_plugin(self, plugin):
        plugin_ok = True
        
        # Check if already registered
        if plugin.name in self.plugin_instances:
            self.log("Attempted to register plugin '" + plugin.name + "', but it already exists", 'error')
            plugin_ok = False
        
        return plugin_ok

    def set_logger(self, logger):
        self.logger = logger
        for hook in self.hook_names:
            self.hooks[hook].set_logger(self.logger)

    def get_logger(self):
        return self.logger

    def log(self, text, level):
        if self.logger is not None:
            self.logger.write(text, level)
        else:
            if level == 'warn':
                text = "[WARNING]: " + text
            if level == 'error':
                text = "[ERROR]: " + text
            print(text)

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
    plugin_handler.hooks["pre-job_execution"].execute({"test":"This is a test"})
    '''
