from ..common.response import Response, StatusCode
from ..common.util import OC2Cmd
from .decorators import target


profile_registry = {
    'NSID': 'x-acme',
    'VERSIONS': ['1.0'],
    'PAIRS': []  # Auto-populated with action-target pairs below.
}


@target('x-acme:road_runner')
def locate(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Road Runner has been located!'
    )


@target('x-acme:road_runner')
def detonate(cmd: OC2Cmd):
    return Response(
        status=StatusCode.INTERNAL_ERROR,
        status_text='INTERNAL ERROR! Now targeting Coyote!!'
    )


@target('properties')
def set(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Properties have been set on x-acme.'
    )


@target('device')
def restart(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Device has been restarted'
    )


@target('device')
def start(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Device is started'
    )


@target('device')
def stop(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Device has been stopped'
    )
