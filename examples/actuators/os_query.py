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


config = ConfigParser()
config.read('osquery_conf.conf')
v = config['path']
os_query = Actuator(nsid='os_query')
orm = OsQueryDatabase(f'{v}/.osquery/osqueryd.sock')
orm.connect()


@os_query.pair('query', 'os_version', implemented=True)
def query_os_version(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    result = orm.tables._cross_platform.OS_Version.select()
    if result.status.code != 0:
        return OpenC2RspFields("error performing osquery function")
    result=list(result)
    return OpenC2RspFields(status=StatusCode.OK, status_text=result)


