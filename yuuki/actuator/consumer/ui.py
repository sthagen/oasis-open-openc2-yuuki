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
        {c.BOLD}Start a proxy server to receive then dispatch OpenC2 Commands{c.END}
            {c.DEFAULT}Defaults{c.END} are sourced from {c.BOLD}yuuki.conf{c.END}
            ''')

        self.parser = argparse.ArgumentParser(
            description=desc,
            usage='%(prog)s [--enpoint ENDPOINT]',
            add_help=False,
            formatter_class=argparse.RawDescriptionHelpFormatter)
        
        common_group = self.parser.add_argument_group(f'{c.BOLD}OPTIONS{c.END}')

        common_group.add_argument(
            '-e',
            '--endpoint',
            default=Config.defaults.endpoint,
            help=f'Server Socket ({c.DEFAULT}{Config.defaults.endpoint}{c.END})')

        common_group.add_argument(
            '-c',
            '--cert',
            default=os.path.join(os.getcwd(), 'certs', 'yuuki.cert'),
            help='Path to SSL Certificate to use for HTTPS')

        common_group.add_argument(
            '-k',
            '--key',
            default=os.path.join(os.getcwd(), 'certs', 'yuuki.key'),
            help='Path to SSL Key to use for HTTPS')

        common_group.add_argument(
            '-h',
            '--help',
            action='store_true')

    def get_opts(self, args: list = None) -> argparse.Namespace:
        if args:
            return self.parser.parse_args(args=args)
        
        options, fluff = self.parser.parse_known_args()
        return options

    def check_ssl(self, cert_path: str, key_path: str) -> Tuple[str, str]:
        if not os.path.isfile(cert_path) or not os.path.isfile(key_path):
            print("SSL files are not found!!")
            rsp = (input(f"Generate self-signed certificates in `{cert_path}`? [Y/n]") or 'Y').lower()
            if rsp == 'y':
                # create a key pair
                k = crypto.PKey()
                k.generate_key(crypto.TYPE_RSA, 2048)

                # create a self-signed cert
                cert = crypto.X509()
                cert.get_subject().C = "US"
                cert.get_subject().O = "Yuuki"
                cert.get_subject().OU = "Yuuki"
                # cert.get_subject().CN = gethostname()
                cert.set_serial_number(1000)
                cert.gmtime_adj_notBefore(0)
                cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
                cert.set_issuer(cert.get_subject())
                cert.set_pubkey(k)
                cert.sign(k, 'sha256')

                pathlib.Path(os.path.dirname(cert_path)).mkdir(parents=True, exist_ok=True)
                open(cert_path, "wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))

                pathlib.Path(os.path.dirname(key_path)).mkdir(parents=True, exist_ok=True)
                open(key_path, "wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
                return cert_path, key_path

            print("Cannot start HTTPS without SSL certificates, Good Bye")
            exit(1)

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
            ssl['ssl_context'] = self.check_ssl(opts.cert, opts.key)
        
        proxy.run(host=endpoint.hostname, port=endpoint.port, **ssl)


def run():
    ui = UI()
    ui.run()
