import ipfshttpclient
import os
import warnings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_ipfs():
    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')
        logger.info("Successfully connected to IPFS")
        return client
    except ipfshttpclient.exceptions.ConnectionError as e:
        logger.warning(f"Failed to connect to IPFS: {str(e)}. Using local storage fallback.")
        return None

def upload_to_ipfs(file_path):
    client = connect_to_ipfs()
    if client:
        try:
            res = client.add(file_path)
            logger.info(f"File uploaded to IPFS with hash: {res['Hash']}")
            return res['Hash']
        except Exception as e:
            logger.error(f"Error uploading to IPFS: {str(e)}")
            return _fallback_to_local_storage(file_path)
        finally:
            client.close()
    else:
        return _fallback_to_local_storage(file_path)

def retrieve_from_ipfs(file_hash, save_path):
    if file_hash.startswith("local:"):
        return _retrieve_from_local_storage(file_hash, save_path)

    client = connect_to_ipfs()
    if client:
        try:
            client.get(file_hash, save_path)
            logger.info(f"File retrieved from IPFS: {file_hash}")
            return save_path
        except Exception as e:
            logger.error(f"Error retrieving from IPFS: {str(e)}")
            raise
        finally:
            client.close()
    else:
        raise Exception("IPFS is not available and file is not stored locally")

def _fallback_to_local_storage(file_path):
    local_storage_path = os.path.join('local_storage', os.path.basename(file_path))
    os.makedirs(os.path.dirname(local_storage_path), exist_ok=True)
    os.replace(file_path, local_storage_path)
    logger.info(f"File stored locally: {local_storage_path}")
    return f"local:{local_storage_path}"

def _retrieve_from_local_storage(file_hash, save_path):
    local_path = file_hash[6:]
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    os.replace(local_path, save_path)
    logger.info(f"File retrieved from local storage: {save_path}")
    return save_path