import ipfshttpclient
import warnings

def upload_to_ipfs(file_path):
    try:
        with ipfshttpclient.connect() as client:
            res = client.add(file_path)
            return res['Hash']
    except ipfshttpclient.exceptions.VersionMismatch:
        warnings.warn("IPFS version mismatch. File will not be uploaded to IPFS.")
        return f"local:{file_path}"
    except Exception as e:
        warnings.warn(f"Error uploading to IPFS: {str(e)}")
        return f"local:{file_path}"

def retrieve_from_ipfs(ipfs_hash, save_path):
    if ipfs_hash.startswith("local:"):
        return ipfs_hash[6:]
    try:
        with ipfshttpclient.connect() as client:
            client.get(ipfs_hash, save_path)
    except ipfshttpclient.exceptions.VersionMismatch:
        warnings.warn("IPFS version mismatch. Unable to retrieve file from IPFS.")
        return None
    except Exception as e:
        warnings.warn(f"Error retrieving from IPFS: {str(e)}")
        return None