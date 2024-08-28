import ipfshttpclient
import os
import warnings

def connect_to_ipfs():
    try:
        return ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
    except ipfshttpclient.exceptions.ConnectionError:
        warnings.warn("Failed to connect to IPFS. Using local storage fallback.")
        return None

def upload_to_ipfs(file_path):
    client = connect_to_ipfs()
    if client:
        try:
            res = client.add(file_path)
            return res['Hash']
        finally:
            client.close()
    else:
        # Fallback to local storage
        local_storage_path = os.path.join('local_storage', os.path.basename(file_path))
        os.makedirs(os.path.dirname(local_storage_path), exist_ok=True)
        os.replace(file_path, local_storage_path)
        return f"local:{local_storage_path}"

def retrieve_from_ipfs(file_hash, save_path):
    if file_hash.startswith("local:"):
        # File is stored locally
        local_path = file_hash[6:]
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        os.replace(local_path, save_path)
        return save_path

    client = connect_to_ipfs()
    if client:
        try:
            client.get(file_hash, save_path)
            return save_path
        finally:
            client.close()
    else:
        raise Exception("IPFS is not available and file is not stored locally")