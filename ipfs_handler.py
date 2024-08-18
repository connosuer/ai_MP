import ipfshttpclient

def upload_to_ipfs(file_path):
    with ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') as client:
        res = client.add(file_path)
        return res['Hash']

def retrieve_from_ipfs(ipfs_hash, save_path):
    with ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') as client:
        client.get(ipfs_hash, save_path)