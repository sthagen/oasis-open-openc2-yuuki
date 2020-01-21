from importlib import import_module
from ..common.util import OC2Cmd, Pair
from ..common.response import Response, StatusCode

# Set which profile(s) are in use. Currently, only one allowed at a time!
ACTIVE_PROFILES = ['profile_acme_anti_roadrunner']
ALLOWED_PROFILE_COUNT = 1


NSIDS = []
PAIRS = {}
VERSIONS = []
RATE_LIMIT = 30  # Magic!


class _ProfileModule:
    def __init__(self, file_name):
        self.NSID = None
        self.file_name = file_name
        self.module = None
        self.PAIRS = []
        self.VERSIONS = None

_profile_count = 0
for profile_name in ACTIVE_PROFILES:
    _profile_count += 1
    if _profile_count > ALLOWED_PROFILE_COUNT:
        raise ValueError('Currently, only one actuator profile can be implemented at a time.')
    
    profile_module = _ProfileModule(profile_name)

    profile_module.module = import_module('.' + profile_name, package='yuuki.actuator.profiles')
    
    profile_registry = getattr(profile_module.module,'profile_registry')
    
    profile_module.NSID = profile_registry['NSID']
    profile_module.PAIRS = profile_registry['PAIRS'].copy()
    profile_module.VERSIONS = profile_registry['VERSIONS'].copy()
   
    if profile_module.NSID in NSIDS:
        raise ValueError('Duplicate profile (nsid)')
    NSIDS.append(profile_module.NSID)

    for pair in profile_module.PAIRS:
        if pair in PAIRS.keys():
            PAIRS[pair].append(profile_module)
        else:
            PAIRS[pair] = [profile_module]
    
    if not VERSIONS:
        VERSIONS = sorted(profile_module.VERSIONS.copy())
    else:
        if VERSIONS != sorted(profile_module.VERSIONS):
            raise ValueError(f'The profiles this actuator implements '
                             f'must all support the same version(s).')


def _handle_query_features(cmd: OC2Cmd):
    results = {
        'versions': VERSIONS,
        'profiles': NSIDS,
        'rate_limit': RATE_LIMIT,
        'pairs': sorted(
            sorted(
                list(set(PAIRS.keys())),
                key=lambda x: x[1]),
            key=lambda x: x[0]
        )
    }
    
    return Response(status=StatusCode.OK, results=results)


def do_it(pair, oc2_cmd, nsid = None):
    """
    Interface to use by external calls.
    """

    # We handle 'query features' here, instead of in a profile module,
    # because a profile module only knows about itself.
    if pair == ('query', 'features'):
        return _handle_query_features(oc2_cmd)
    
    funcs = funcs_to_call(oc2_cmd)

    if len(funcs) == 0:
        return Response(status=StatusCode.BAD_REQUEST,
                        status_text='No response would be generated')
    elif len(funcs) == 1:
        return funcs[0](oc2_cmd)
    else:
        oc2_response = Response()
        oc2_response.results = {}
        
        for func in funcs:
            oc2_response.results[profile_module.NSID] = func(oc2_cmd)
        
        lowest_status = StatusCode.OK
        for _oc2_rsp in oc2_response.results.values():
            if _oc2_rsp.status.value > lowest_status.value:
                lowest_status = _oc2_rsp.status
        
        oc2_response.status = lowest_status
        return oc2_response

def funcs_to_call(oc2_cmd):
    action  = oc2_cmd.action
    target, = oc2_cmd.target.keys()
    pair = Pair(action, target)
    actuator_nsid = None
    if oc2_cmd.actuator is not None:
        actuator_nsid, = oc2_cmd.actuator.keys()
    
    if pair not in PAIRS.keys():
        return []
    elif actuator_nsid != None:
        for profile_module in PAIRS[pair]:
            if profile_module.NSID == actuator_nsid:
                return [getattr(profile_module.module, pair.action)]
        return []
    else:
        retval = []
        for profile_module in PAIRS[pair]:
            retval.append(getattr(profile_module.module, pair.action))
        return retval