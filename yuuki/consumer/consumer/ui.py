import argparse
import os
import pathlib
import textwrap

from OpenSSL import crypto, SSL
from urllib.parse import urlparse

from typing import (
    Optional,
    Tuple
)

from ...config import Config
from . import proxy


class UI:
    def __init__(self):
        """
        """
        c = Config.Console

        desc = textwrap.dedent(f'''\
        {c.BOLD}Start a Consumer process to receive then dispatch OpenC2 Commands{c.END}
            {c.DEFAULT}Defaults{c.END} are sourced from {c.BOLD}yuuki.conf{c.END}
            ''')

        self.parser = argparse.ArgumentParser(
            description=desc,
            usage='%(prog)s [--enpoint ENDPOINT]',
            add_help=False,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog='yuuki.consumer')
        
        common_group = self.parser.add_argument_group(f'{c.BOLD}OPTIONS{c.END}')

        common_group.add_argument(
            '-e',
            '--endpoint',
            default=Config.defaults.endpoint,
            help=f'Server Socket ({c.DEFAULT}{Config.defaults.endpoint}{c.END})')

        common_group.add_argument(
            '-h',
            '--help',
            action='store_true')

    def get_opts(self, args: list = None) -> argparse.Namespace:
        if args:
            return self.parser.parse_args(args=args)
        
        options, fluff = self.parser.parse_known_args()
        return options

    def run(self):
        """
        """
        opts = self.get_opts()
        if opts.help:
            self.parser.print_help()
            return

        # Parse http://127.0.0.1:9001
        endpoint = urlparse(opts.endpoint)
        ssl = {}

        if endpoint.scheme.lower() == "https":
            ssl['ssl_context'] = 'adhoc'
        
        proxy.run(host=endpoint.hostname, port=endpoint.port, **ssl)


def run():
    ui = UI()
    ui.run()
