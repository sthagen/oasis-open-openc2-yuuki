"""Profile for SBOM Version 1.0
https://github.com/oasis-tcs/openc2-ap-SBOM/blob/published/ap-SBOM-v1.0-wd01.html
Conformant to Conformance Clauses ?
"""
import json
import os
from pathlib import Path
from oc2_arch import Actuator, OpenC2CmdFields, OpenC2RspFields, StatusCode

sbom = Actuator(nsid='sbom')

sbom_formats = {
    "cyclonedx": os.path.join(Path(__file__).resolve().parent, "CycloneExample.bom.1.3.json"),
    "cyclone": os.path.join(Path(__file__).resolve().parent, "CycloneExample.bom.1.3.json"),
    "spdx2": os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json"),
    "default": os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")
}

    #These functions will be changed when there is knowledge of the Actions or Targets involved in SBOM


@sbom.pair('query', 'sbom', implemented=True)
def query_sbom(oc2_cmd: OpenC2CmdFields) ->OpenC2RspFields:

    query_fields = oc2_cmd.target.get("sbom", {})
    print(query_fields)

    if c := query_fields.pop("content", None):
        for element in c:
            if element == "cyclonedx":
                sbom_file = os.path.join(Path(__file__).resolve().parent, "CycloneExample.bom.1.3.json")
            elif element == "cyclone":
                sbom_file = os.path.join(Path(__file__).resolve().parent, "CycloneExample.bom.1.3.json")
            elif element == "spdx2":
                sbom_file = os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")
            else:
                sbom_file = os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")
    else:
        sbom_file = os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")

    if os.path.exists(sbom_file):
        with open(sbom_file, "r") as f:
            print("Printing "+sbom_file)
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
    
        #_type = query_fields.pop("type", "default")
    #sbom_file = sbom_formats.get(_type, sbom_formats["default"])

    #if _content := query_fields.pop("content", None):
       #pass
    
        if y := query_fields.pop("cyclonedx"):
        sbom_file = os.path.join(Path(__file__).resolve().parent, "CycloneExample.bom.1.3.json")
    elif y := query_fields.pop("cyclone"):
        sbom_file = os.path.join(Path(__file__).resolve().parent, "CycloneExample.bom.1.3.json")
    elif y := query_fields.pop("spdx2"):
        sbom_file = os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")
    else:
        sbom_file = os.path.join(Path(__file__).resolve().parent, "SPDXJSONExample-v2.2.spdx.json")
    """
