import time
import jwt

# Open PEM
private_key = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEIGdbNnIbH3Zryz0eYeedlB5nv34/5rwLfQ76jkUa9Lks
-----END PRIVATE KEY-----"""

payload = {
    'iat': int(time.time()) - 30,
    'exp': int(time.time()) + 900,
    'sub': '4GKREU7KJ9'
}
headers = {
    'kid': 'KNPKEKX93G'
}

# Generate JWT
encoded_jwt = jwt.encode(payload, private_key, algorithm='EdDSA', headers=headers)

# print(f"JWT:  {encoded_jwt}")
