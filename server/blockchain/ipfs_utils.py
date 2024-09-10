import ipfshttpclient

def connect_to_ipfs():
    """
    Connect to IPFS
    """
    return ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

def add_to_ipfs(data):
    """
    Add to IPFS
    """
    client = connect_to_ipfs()
    res = client.add_json(data)
    return res

def get_from_ipfs(cid):
    """
    Getting from the IPFS
    """
    client = connect_to_ipfs()
    return client.get_json(cid)