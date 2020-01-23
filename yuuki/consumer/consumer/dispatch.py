from .validate import convert_raw_cmd
from .. import profiles
from ..common.response import StatusCode, Response
from ..common.util import OC2Cmd, Pair, OC2Exception


class Dispatcher:
    def dispatch(self, raw_cmd: dict):
        """
        Receive a command; dispatch to a profile module based on pair.

        All calls to this expect to receive an OpenC2 Response!
        Well, response_requested=none is an outlier..
        """
        try:
            oc2_cmd = convert_raw_cmd(raw_cmd)
        except OC2Exception as e:
            return Response(
                status=StatusCode.BAD_REQUEST,
                status_text=str(e)
            )
        except Exception as e:
            return Response(
                status=StatusCode.INTERNAL_ERROR,
                status_text=str(e)
            )

        # We a have a correctly formatted OC2Cmd now.
        action  = oc2_cmd.action
        target, = oc2_cmd.target.keys()
        pair = Pair(action, target)
        
        # 'ack' and 'status' in response_requested requires
        # some form of concurrency that we haven't implemented.
        # So we don't dispatch to a profile, and instead return
        # Not Implemented. 'none' requires more control over
        # our web-server that we don't have.
        response_requested = self._get_response_requested(oc2_cmd)
        if response_requested in ['none', 'ack', 'status']:
            return Response(
                status=StatusCode.NOT_IMPLEMENTED,
                status_text="Only response_requested = 'complete' is currently implemented."
            )
        
        # Same for any timing requests.
        if self._is_timing_important(oc2_cmd):
            return Response(
                status=StatusCode.NOT_IMPLEMENTED,
                status_text="'start_time', 'stop_time', and 'duration' are not currently implemented."
            )

        oc2_response = profiles.do_it(pair, oc2_cmd)

        return oc2_response
    
    def _get_response_requested(self, cmd: OC2Cmd):
        if cmd.args is not None:
            return cmd.args.get('response_requested', 'complete')
        return 'complete'
    
    def _is_timing_important(self, cmd: OC2Cmd):
        if cmd.args is not None:
            return any([x in ['start_time', 'stop_time', 'duration'] for x in cmd.args.keys()])
        return False
