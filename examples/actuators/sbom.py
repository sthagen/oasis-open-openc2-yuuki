"""Profile for SBOM Version 1.0
https://github.com/oasis-tcs/openc2-ap-SBOM/blob/published/ap-SBOM-v1.0-wd01.html
Conformant to Conformance Clauses ?
"""
import json
import os
from pathlib import Path
from yuuki import Actuator, OpenC2CmdFields, OpenC2RspFields, StatusCode

sbom = Actuator(nsid='sbom')


    #These functions will be changed when there is knowledge of the Actions or Targets involved in SBOM


@sbom.pair('query', 'sbom', implemented=True)
def query_sbom(oc2_cmd: OpenC2CmdFields):
    sbom_file = os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")
    if os.path.exists(sbom_file):
        with open(sbom_file, "r") as f:
            print(f"opening SPDXJSONExample-v2.2.spdx.json")
            sbom: dict = json.load(f)
        return OpenC2RspFields(status=StatusCode.OK, results=sbom)
    return OpenC2RspFields(status=StatusCode.NOT_FOUND, status_text="error performing SBOM retrieval")




"""
@sbom.pair('query', 'supplier', implemented=False)
def get_supplier(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@sbom.pair('query', 'component_name', implemented=False)
def get_component_name(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@sbom.pair('query', 'version', implemented=False)
def get_version(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@sbom.pair('query', 'unique_IDs', implemented=False)
def get_unique_IDs(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@sbom.pair('query', 'dependencies', implemented=False)
def get_dependencies(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'author', implemented=False)
def get_author(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'timestamp', implemented=False)
def get_timestamp(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'supplier', implemented=False)
def get_supplier(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass
    """
