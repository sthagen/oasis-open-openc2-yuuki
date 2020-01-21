import argparse
import json
import re
import sys
import textwrap

try:
    from importlib import resources
except ImportError:
    import importlib_resources as resources

from ..config import Config
from . import (
    data,
    network
)


class UI:
    def __init__(self):
        c = Config.Console
        self.json_cmds = {}
        self.parser = argparse.ArgumentParser(
            usage="%(prog)s [options] <command> [sub-options]",
            add_help=False,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='yuuki.producer'
        )

        self.parser.description = textwrap.dedent(f"""
            {c.BOLD}Send OpenC2 commands to a Consumer endpoint{c.END}
                {c.DEFAULT}Defaults{c.END} are sourced from {c.BOLD}yuuki.conf{c.END}

            {c.BOLD}EXAMPLES:{c.END}
                Manually type and send an OpenC2 command:
                    > {self.parser.prog} type-it
                    > {{
                    > "action" : "deny",
                    > "target" : {{"domain_name" : "evil.com"}}
                    > }}

                Send OpenC2 'query-features' command from the examples file:
                    > {self.parser.prog} send query-features

                Show all OpenC2 commands from the examples file:
                    > {self.parser.prog} show
            """)

        # Common Args
        common_group = self.parser.add_argument_group(f"{c.BOLD}OPTIONS{c.END}")
        endpoint_help = f"({c.DEFAULT}{Config.defaults.endpoint}{c.END}) Remote socket"
        common_group.add_argument("-e", "--endpoint", default=Config.defaults.endpoint, help=endpoint_help)
        common_group.add_argument("-h", "--help", default=False, action="store_true", help="Show help and exit")

        # Sub Commands
        subparsers = self.parser.add_subparsers(
            title=f"{c.BOLD}COMMANDS{c.END}",
            dest="cmd",
            metavar=""
        )

        # Type-It command
        type_it_cmd = subparsers.add_parser(
            "type-it",
            help="Manually type and send a command",
            usage="type-it [type-it-options]"
        )
        type_it_cmd.set_defaults(func=self.cmd_send_from_cli)

        # Send command
        send_cmd = subparsers.add_parser(
            "send",
            help="Send a cmd from example_commands.json",
            usage="send [cmd-name]"
        )
        self.json_cmds = self._get_json_cmds()
        send_cmd.add_argument('cmd_name', choices=[*self.json_cmds.keys()])
        send_cmd.set_defaults(func=self.cmd_send_from_file)

        # Show command
        show_cmd = subparsers.add_parser(
            "show",
            help="Display the cmds found in example_openc2_commands.json file",
            usage="show [show-options]"
        )
        show_cmd.set_defaults(func=self.cmd_show)

    def _get_json_cmds(self):
        stream = resources.open_text('yuuki.client.data', 'example_openc2_commands.json')
        cmds_dict = json.load(stream)
       
        # While we're here, get some formatting info to use when displaying...
        max_cmd_name_len = 1
        max_action_len = 1
        max_target_len = 1
        
        for cmd_name, cmd in cmds_dict.items():
            max_cmd_name_len = max(len(cmd_name), max_cmd_name_len)
            max_action_len = max(len("action" + str(cmd["action"])), max_action_len)
            max_target_len = max(len("target" + str(cmd["target"])), max_target_len)
        
        # Pad with extra formatting characters e.g. "{ , etc
        self.max_cmd_name_len = max_cmd_name_len + 2
        self.max_action_len = max_action_len + 8
        self.max_target_len = max_target_len + 6

        return cmds_dict

    def parse_args(self, args: list = None) -> argparse.Namespace:
        if args:
            return self.parser.parse_args(args=args or ["--help"])
        
        options, args = self.parser.parse_known_args()
        return options    

    def _color_cmd(self, input):
        tags = ['action', 'target', 'args', 'actuator', 'command_id']
        return self._color_tags(input, tags, Config.Console.COMMAND)
    
    def _color_response(self, input):
        tags = ['status', 'status_text', 'results']
        return self._color_tags(input, tags, Config.Console.RESPONSE)

    def _color_tags(self, input, tags, color):
        for item in tags:
            pattern = f'(?<="){item}(?=":)'
            replace_with = f'{color}{item}{Config.Console.END}'
            input = re.sub(pattern, replace_with, input)
        return input

    def _send(self, endpoint: str, cmd: dict) -> None:
        c = Config.Console
        print()
        print(f'>>> {c.COMMAND}COMMAND{c.END}')

        visible_cmd = json.dumps(cmd, indent=3)
        print(self._color_cmd(visible_cmd))
        print()

        response = network.send(endpoint, cmd)

        print(f'<<< {c.RESPONSE}RESPONSE{c.END}')
        visible_response = json.dumps(response.json(), indent=3)
        print(self._color_response(visible_response))
        print()

    def cmd_send_from_file(self, opts: argparse.Namespace) -> None:
        if not opts.cmd_name:
            print('Supply a command name from the json file, e.g. query-features')
            return None
        try:
            cmd = self.json_cmds[opts.cmd_name]
        except Exception as e:
            print(e)
            return None
        self._send(opts.endpoint, cmd)

    def cmd_send_from_cli(self, opts: argparse.Namespace) -> None:
        c = Config.Console
        
        print(textwrap.dedent(f"""
            {c.BOLD}Enter a [multi-line] JSON-formatted OpenC2 command.{c.END}
            (hit Enter when done, or Enter now to see an example.)
        """))

        prompt = ""
        cmd = ""

        try:
            for line in iter(lambda: input(prompt), ""):
                cmd += line
        except KeyboardInterrupt:
            return None
        
        if len(cmd) < 1:
            fmt_cmd = {"action": "deny", "target": {"domain_name": "evil.com"}}
            print(f"{c.BOLD}Example:{c.END}\n")
            print(json.dumps(fmt_cmd, indent=3))
            return None
        
        if not cmd.startswith('{'):
            cmd = '{' + cmd
        if not cmd.endswith('}'):
            cmd += '}'
        
        try:
            cmd = json.loads(cmd)
        except json.decoder.JSONDecodeError as e:
            print(f"Could not parse JSON: {e}")
            return None

        self._send(opts.endpoint, cmd)

    def cmd_show(self, opts: argparse.Namespace) -> None:
        
        def align_action_target(cmd_name, cmd):
            action, target, suffix = cmd.split(',', maxsplit=2)
            cmd_len = self.max_cmd_name_len
            act_len = self.max_action_len
            tar_len = self.max_target_len
            retval = '{0:<{cmd_len}}{1:<{act_len}}{2:<{tar_len}}{3}'.format(cmd_name, 
                                                                            action + ',',
                                                                            target + ',',
                                                                            suffix, 
                                                                            cmd_len=cmd_len,
                                                                            act_len=act_len,
                                                                            tar_len=tar_len)
            
            return retval

        for cmd_name, cmd in self.json_cmds.items():
            print(self._color_cmd(align_action_target(cmd_name,json.dumps(cmd))))
    
    def run(self) -> None:
        opts = self.parse_args()

        # Check for basic sanity
        if not opts.cmd and opts.help:
            self.parser.print_help()
        elif not opts.cmd:
            self.parser.print_usage()
        else:
            opts.func(opts)


def run():
    # Disable warning from requests module about certificate verification.
    if not sys.warnoptions:
        import warnings
        warnings.simplefilter("ignore")
    ui = UI()
    ui.run()
