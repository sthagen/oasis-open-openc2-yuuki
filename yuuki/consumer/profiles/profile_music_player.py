from ..common.response import Response, StatusCode
from ..common.util import OC2Cmd
from .decorators import target


profile_registry = {
    'NSID': 'x-music',
    'VERSIONS': ['1.0'],
    'PAIRS': []  # Auto-populated
}


@target('x-music:song')
def start(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Started a song...'
    )


@target('x-music:song')
def stop(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Stopped a song...'
    )

@target('properties')
def set(cmd: OC2Cmd):
    return Response(
        status=StatusCode.OK,
        status_text='Properties have been set on x-music.'
    )