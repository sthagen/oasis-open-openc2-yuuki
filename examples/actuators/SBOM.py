"""Profile for SBOM Version 1.0
https://github.com/oasis-tcs/openc2-ap-SBOM/blob/published/ap-SBOM-v1.0-wd01.html
Conformant to Conformance Clauses ?
"""

from yuuki import Actuator, OpenC2CmdFields, OpenC2RspFields, StatusCode

SBOM = Actuator(nsid='SBOM')


    #These functions will be changed when there is knowledge of the Actions or Targets involved in SBOM


@SBOM.pair('query', 'SBOM', implemented=True)
def query_SBOM(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    sbom = open("examples/actuators/SPDXJSONExample-v2.2.spdx.json", "r")
    print(f"opening SPDXJSONExample-v2.2.spdx.json")
    bom = list(sbom)
    sbom.close()
    if bom:
        return OpenC2RspFields(status=StatusCode.OK, status_text=str(bom))
    else:
        return OpenC2RspFields(status=StatusCode.NOT_FOUND, status_text="error performing SBOM retrieval")




"""
@SBOM.pair('get', 'supplier', implemented=False)
def get_supplier(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'component_name', implemented=False)
def get_component_name(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'version', implemented=False)
def get_version(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'unique_IDs', implemented=False)
def get_unique_IDs(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@SBOM.pair('get', 'dependencies', implemented=False)
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
