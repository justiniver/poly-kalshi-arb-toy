import os
from dotenv import load_dotenv
import requests
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

def sign_request(private_key, timestamp, method, path):
    # Strip query parameters from path before signing
    path_without_query = path.split('?')[0]

    # Create the message to sign
    message = f"{timestamp}{method}{path_without_query}".encode('utf-8')

    # Sign with RSA-PSS
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.DIGEST_LENGTH
        ),
        hashes.SHA256()
    )

    # Return base64 encoded
    return base64.b64encode(signature).decode('utf-8')

load_dotenv()
KALSHI_ACCESS_KEY = os.getenv('KALSHI_ACCESS_KEY')
KALSHI_PRIVATE_KEY = os.getenv('KALSHI_PRIVATE_KEY')
timestamp = str(int(datetime.datetime.now().timestamp() * 1000))

signature = sign_request(KALSHI_PRIVATE_KEY, timestamp, method, path)

url = "https://api.elections.kalshi.com/trade-api/v2/portfolio/order_groups"

headers = {
    "KALSHI-ACCESS-KEY": KALSHI_ACCESS_KEY,
    "KALSHI-ACCESS-SIGNATURE": "<api-key>",
    "KALSHI-ACCESS-TIMESTAMP": timestamp
}

response = requests.get(url, headers=headers)

print(response.json())
