"""internal test for os query use
"""

import osquery

from osquery_orm.tables import Tables
from pathlib import Path
from configparser import ConfigParser
from osquery_orm import OsQueryDatabase
from osquery.extension_client import Client
from peewee import Database, SQL, ColumnMetadata, ForeignKeyMetadata, IndexMetadata, ProgrammingError, fn, simple_date_time

from yuuki import Actuator, OpenC2CmdFields, OpenC2RspFields, StatusCode

# Common OSQuery tables and their fields
Common_Tables = ("arp_cache", "atom_packages", "azure_instance_metadata", "azure_instance_tags", "carbon_black_info",
                 "carves", "chrome_extension_content_scripts", "chrome_extensions", "cpuid", "curl", "curl_certificate",
                 "ec2_instance_metadata", "ec2_instance_tags", "etc_hosts", "etc_protocols", "etc_services", "example",
                 "file", "firefox_addons", "groups", "hash", "intel_me_info", "interface_addresses", "interface_details",
                 "kernel_info", "listening_ports", "logged_in_users", "os_version", "osquery_events",
                 "osquery_extensions", "osquery_flags", "osquery_info", "osquery_packs", "osquery_registry",
                 "osquery_schedule", "platform_info", "process_memory_map", "process_open_sockets", "processes",
                 "python_packages", "routes", "secureboot", "ssh_configs", "startup_items", "system_info", "time",
                 "uptime", "user_groups", "user_ssh_keys", "users", "ycloud_instance_metadata")



config = ConfigParser()
config.read('osquery_conf.conf')
v = config['path']
os_query = Actuator(nsid='os_query')
orm = OsQueryDatabase(f'{v}/.osquery/osqueryd.sock')
orm.connect()
t = ""
f = []
db = []


@os_query.pair('query', 'database', implemented=True)
def query_database(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    query_fields = {oc2_cmd.target.values()}
    if (db := query_fields.pop("database", None)) and db == "system":

            for k, v in query_fields():
                if v in Common_Tables: t = v
                elif v == "filters": f = v
                else: return OpenC2RspFields("error performing db function, unknown aguments")
                result = orm.tables._cross_platform.t.select()
                if result.status.code != 0:
                    return OpenC2RspFields("error performing osquery function")
                else:
                    r = list(result)
                    return OpenC2RspFields(status=StatusCode.OK, status_text=r)
    else: return OpenC2RspFields("error performing osquery function: table improperly specified.")










"""
@os_query.pair('query', 'os_version', implemented=True)
def query_os_version(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    result = orm.tables._cross_platform.OS_Version.select()
    if result.status.code != 0:
        return OpenC2RspFields("error performing osquery function")
    result=list(result)
    return OpenC2RspFields(status=StatusCode.OK, status_text=result)

older version from when we were returning multiple wueries per command
@os_query.pair('query', 'file', implemented=True)
def query_os_version(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    result = ""
    for key in oc2_cmd.target:
        result.__add__(orm.tables._cross_platform.file.select(key, oc2_cmd.target.values()))
        if result.status.code != 0:
            return OpenC2RspFields("error performing osquery function")
    result = list(result)
    return OpenC2RspFields(status=StatusCode.OK, status_text=result)

"""