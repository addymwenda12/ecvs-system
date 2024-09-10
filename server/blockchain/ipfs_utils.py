import ipfshttpclient

def connect_to_ipfs():
    """
    Connect to IPFS
    """
    try:
        return ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    except Exception as e:
        print(f"Error connecting to IPFS: {str(e)}")
        return None

def add_to_ipfs(data):
    """
    Add to IPFS
    """
    client = connect_to_ipfs()
    if client:
        res = client.add_json(data)
        # Publish to IPNS
        client.name.publish(res['Hash'])
        return res
    return None

def get_from_ipfs(cid):
    """
    Getting from the IPFS
    """
    client = connect_to_ipfs()
    if client:
        # Resolve IPNS name if necessary
        if cid.startswith('Qm'):
            return client.get_json(cid)
        else:
            resolved = client.name.resolve(cid)
            return client.get_json(resolved['Path'])
    return None