import socket
import json

# rig host list
hostList = ['192.168.1.141', '192.168.1.136']
# port for host address
port = 3333


def getRigStatus(host, port):
    """
    Gets json values for rig given the host and port number
    returns None if connection fails

    return array values:
    0: Miner version
    1: Running time, in minutes
    2: total ETH hashrate in MH/s, number of ETH shares, number of ETH
       rejected shares.
    3: detailed ETH hashrate for all GPUs.
    4: total DCR hashrate in MH/s, number of DCR shares, number of DCR
       rejected shares.
    5: detailed DCR hashrate for all GPUs.
    6: Temperature and Fan speed(%) pairs for all GPUs.
    7: current mining pool. For dual mode, there will be two pools here.
    8: number of ETH invalid shares, number of ETH pool switches, number of
       DCR invalid shares, number of DCR pool switches.

    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
    except socket.error, exc:
        print "Caught exception socket.error : %s" % exc
        return

    # get rig status
    s.sendall(b'{"id":0, "jsonrpc": "2.0", "method": "miner_getstat1"}')
    data = s.recv(1024)
    s.close()

    try:
        decoded = json.loads(data)['result']
        return decoded

    except (ValueError, KeyError, TypeError):
        print "JSON format error"
        return None


def reportStatus(host, port):
    status = getRigStatus(host, port)
    if status is not None:

        status = str('Status ' + host + '\n'
                     'Miner version: ' + status[0] + '\n'
                     'Running time: ' + status[1] + '\n'
                     'Total Hashrate: ' + status[2] + '\n'
                     'Hashrate per GPU: ' + status[3] + '\n'
                     'Temperature and fan speed: ' + status[6])
        return status

    else:
        print 'No response from', host
