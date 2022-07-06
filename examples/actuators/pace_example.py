import osquery
import nmap
from elasticsearch import Elasticsearch

from oc2_arch import Actuator, OpenC2CmdFields, OpenC2RspFields, StatusCode


pace = Actuator(nsid='x-pace')


@pace.pair('query', 'device')
def query_os_version(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    """
    Custom Actuator profile implementation for getting os version using osquery
    """
    instance = osquery.SpawnInstance()
    instance.open()

    es = Elasticsearch(['http://elastic.olympus.mtn:9200'])

    query = instance.client.query('SELECT * FROM os_version')
    print("QUERY")
    print(query.response[0])

    es.index(index='test3', document=query.response[0])

    return OpenC2RspFields(status=StatusCode.OK)


@pace.pair('query', 'x-pace:ports')
def query_ports(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    """
    Custom Actuator profile implementation for getting processes listening on ports using osquery
    """
    instance = osquery.SpawnInstance()
    instance.open()

    es = Elasticsearch(['http://elastic.olympus.mtn:9200'])

    query = instance.client.query('''
                                  SELECT DISTINCT processes.name, listening_ports.port FROM listening_ports
                                  JOIN processes USING (pid)
                                  WHERE listening_ports.family = 2
                                  AND listening_ports.address <> "127.0.0.1" AND port <> 0
                                  ORDER BY port;
                                  ''')
    query_results = {}
    print(query.response)
    ports = getattr(oc2_cmd.args, 'x-pace').get('ports') if getattr(oc2_cmd.args, 'x-pace') is not None else None
    lower_bound, upper_bound = map(int, ports.split('-'))
    print(lower_bound, upper_bound)
    for pair in query.response:
        print(pair)
        if lower_bound <= int(pair['port']) <= upper_bound:
            print("TEST: ", pair, lower_bound, upper_bound)
            query_results[pair['port']] = pair['name']
    print(query_results)

    es.index(index='test3', document=query_results)

    return OpenC2RspFields(status=StatusCode.OK)


@pace.pair('scan', 'ipv4_net')
def scan_ports(oc2_cmd: OpenC2CmdFields) -> OpenC2RspFields:
    """
    Custom Actuator profile implementation for scanning network using nmap
    """

    es = Elasticsearch(['http://elastic.olympus.mtn:9200'])

    nm = nmap.PortScanner()

    host = oc2_cmd.target['ipv4_net'] if oc2_cmd.target.get('ipv4_net') is not None else oc2_cmd.target['domain_name']
    ports = getattr(oc2_cmd.args, 'x-pace').get('ports') if getattr(oc2_cmd.args, 'x-pace') is not None else None

    nm.scan(host, ports)
    scan_results = {}

    for proto in nm[host].all_protocols():
        lport = list(nm[host][proto].keys())
        lport.sort()
        for port in lport:
            print(f'name : {nm[host][proto][port]["name"]}\tport : {port}')
            scan_results[port] = nm[host][proto][port]["name"]

    print("SCAN RESULTS")
    print(scan_results)
    es.index(index='test3', document=scan_results)

    return OpenC2RspFields(status=StatusCode.OK)
