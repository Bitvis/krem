

import os
from krempack.core import plugin
from krempack.common import kremtree

class TestPluginCliHooks(plugin.Plugin):
    name = "Test-plugin-cli-hooks"

    def __init__(self):
        None
 
    def cli_commands(self, commands):
        commands["test"] = os.path.join(os.path.dirname(__file__), 'test.cmd')

    def cli_init_setup_arguments(self, parser):
        group = parser.add_argument_group()
        group.add_argument("-x", "--test-command", action='store_true',
                           help="test command help string")

    def cli_init_execute_arguments_pre_cmd(self, args):
        print("Executing pre_cmd hook")
        if args.test_command:
            print("Received argument in pre_cmd")

    def cli_init_execute_arguments_post_cmd(self, args):
        print("Executing post_cmd hook")
        if args.test_command:
            print("Received argument in post_cmd")

    def cli_run_setup_arguments(self, parser):
        group = parser.add_argument_group()
        group.add_argument("-x", "--test-command", action='store_true',
                           help="test command help string")

    def cli_run_execute_arguments_pre_cmd(self, args):
        print("Executing pre_cmd hook")
        if args.test_command:
            print("Received argument in pre_cmd")

    def cli_run_execute_arguments_post_cmd(self, args):
        print("Executing post_cmd hook")
        if args.test_command:
            print("Received argument in post_cmd")

    def cli_list_setup_arguments(self, parser):
        group = parser.add_argument_group()
        group.add_argument("-x", "--test-command", action='store_true',
                           help="test command help string")

    def cli_list_execute_arguments_pre_cmd(self, args):
        print("Executing pre_cmd hook")
        if args.test_command:
            print("Received argument in pre_cmd")

    def cli_list_execute_arguments_post_cmd(self, args):
        print("Executing post_cmd hook")
        if args.test_command:
            print("Received argument in post_cmd")