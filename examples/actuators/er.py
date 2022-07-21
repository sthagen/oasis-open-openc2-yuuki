"""Profile for er Version 1.0
https://github.com/oasis-tcs/openc2-ap-er/blob/working/oc2edr.md
Conformant to Conformance Clauses ?
"""
import json
import os
from pathlib import Path
from oc2_arch import Actuator, OpenC2CmdFields, OpenC2RspFields, StatusCode

er = Actuator(nsid='er')




#These functions will be changed when there is knowledge of the Actions or Targets involved in er

@er.pair('allow', 'domain_name', implemented=False)
def allow_domain_name(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('allow', 'device', implemented=False)
def allow_device(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('allow', 'file', implemented=False)
def allow_file(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('allow', 'ipv4_net', implemented=False)
def allow_ipv4_net(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('allow', 'ipv6_net', implemented=False)
def allow_ipv6_net(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    allowed_keys = ['src_addr', 'src_port', 'dst_addr', 'dst_port', 'protocol']
    found_keys = []
    found_other = []
    if isinstance(oc2_cmd.target['ipv6_connection'], dict):
        for key in oc2_cmd.target['ipv6_connection'].keys():
            if key in allowed_keys:
                found_keys.append(key)
            else:
                found_other.append(key)

    if len(found_keys) < 1 or len(found_other) > 0:
        return OpenC2RspFields(status=StatusCode.BAD_REQUEST,
                               status_text=f'Any of {str(allowed_keys)} required for ipv6_connection')

    pass


@er.pair('deny', 'domain_name', implemented=False)
def deny_domain_name(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('deny', 'file', implemented=False)
def file(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass
    

@er.pair('deny', 'ipv4_net', implemented=False)
def deny_ipv4_net(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('deny', 'ipv6_net', implemented=False)
def deny_ipv6_net(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    allowed_keys = ['src_addr', 'src_port', 'dst_addr', 'dst_port', 'protocol']
    found_keys = []
    found_other = []
    if isinstance(oc2_cmd.target['ipv6_connection'], dict):
        for key in oc2_cmd.target['ipv6_connection'].keys():
            if key in allowed_keys:
                found_keys.append(key)
            else:
                found_other.append(key)

    if len(found_keys) < 1 or len(found_other) > 0:
        return OpenC2RspFields(status=StatusCode.BAD_REQUEST,
                               status_text=f'Any of {str(allowed_keys)} required for ipv6_connection')


    pass
    

@er.pair('contain', 'device', implemented=False)
def contain_device(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:

    #args include device_containment, permitted_addresses

    pass


@er.pair('contain', 'file', implemented=False)
def contain_file(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('create', 'registry_entry', implemented=False)
def create_registry_entry(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('delete', 'file', implemented=False)
def delete_file(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('delete', 'registry_entry', implemented=False)
def delete_registry_entry(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass
    

@er.pair('delete', 'service', implemented=False)
def delete_service(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('start', 'file', implemented=False)
def start_file(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('stop', 'device', implemented=False)
def stop_device(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass
    

@er.pair('stop', 'process', implemented=False)
def stop_process(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass  
        

@er.pair('stop', 'service', implemented=False)
def stop_service(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass   
    
    
@er.pair('restart', 'device', implemented=False)
def restart_device(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass
    

@er.pair('restart', 'process', implemented=False)
def restart_process(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass


@er.pair('scan', 'device', implemented=False)
def scan_device(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:

    #args may include scan_depth, periodic_scan

    pass

@er.pair('set', 'ipv4_net', implemented=False)
def set_ipv4_net(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass  
        

@er.pair('set', 'ipv6_net', implemented=False)
def set_ipv6_net(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    allowed_keys = ['src_addr', 'src_port', 'dst_addr', 'dst_port', 'protocol']
    found_keys = []
    found_other = []
    if isinstance(oc2_cmd.target['ipv6_connection'], dict):
        for key in oc2_cmd.target['ipv6_connection'].keys():
            if key in allowed_keys:
                found_keys.append(key)
            else:
                found_other.append(key)

    if len(found_keys) < 1 or len(found_other) > 0:
        return OpenC2RspFields(status=StatusCode.BAD_REQUEST,
                               status_text=f'Any of {str(allowed_keys)} required for ipv6_connection')

    pass   
    
    
@er.pair('set', 'registry_entry', implemented=False)
def set_registry_entry(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass
    

@er.pair('set', 'account', implemented=False)
def set_account(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:

    #requires arg account_status

    pass


@er.pair('update', 'file', implemented=False)
def update_file(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    pass







"""
@er.pair('query', 'er', implemented=True)
def query_er(oc2_cmd: OpenC2CmdFields) ->OpenC2RspFields:

    query_fields = oc2_cmd.target.get("er", {})
    print(query_fields)

    if c := query_fields.pop("content", None):
        for element in c:
            if element == "cyclonedx":
                er_file = os.path.join(Path(__file__).resolve().parent, "files/CycloneExample.bom.1.3.json")
            elif element == "cyclone":
                er_file = os.path.join(Path(__file__).resolve().parent, "files/CycloneExample.bom.1.3.json")
            elif element == "spdx2":
                er_file = os.path.join(Path(__file__).resolve().parent, "files/SPDXJSONExample-v2.2.spdx.json")
            else:
                er_file = os.path.join(Path(__file__).resolve().parent, "files/SPDXJSONExample-v2.2.spdx.json")
    else:
        er_file = os.path.join(Path(__file__).resolve().parent, "files/SPDXJSONExample-v2.2.spdx.json")

    if os.path.exists(er_file):
        with open(er_file, "r") as f:
            print("Printing "+er_file)
            er: dict = json.load(f)
        return OpenC2RspFields(status=StatusCode.OK, results=er)
    return OpenC2RspFields(status=StatusCode.NOT_FOUND, status_text="error performing er retrieval")
"""

