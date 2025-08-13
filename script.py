import random
import os
import requests
from Crypto.Cipher import AES

FLAG = "glovo{this_is_a_fake_flag_for_demo_purposes}"

def blend_key(key_bytes):
    key_int = int(key_bytes.hex(), 16)
    return key_int * random.randint(1, 99999) * random.randint(1, 99999) * random.randint(1, 99999) + 998877665544332211

def create_github_issue(repo,  body, token):
    url = f"https://api.github.com/repos/{repo}/issues/1/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "body": body
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    key = os.getenv("SECRET_KEY").encode()
    iv = b"product_security"
    cipher = AES.new(key, AES.MODE_OFB, iv)
    encrypted_flag = cipher.encrypt(FLAG.encode())
    shuffled_key = blend_key(key)

    body = f"Your shuffled key:\n{shuffled_key}\n\nHere's your encrypted flag:\n{encrypted_flag.hex()}"

    repo = "puckk/testctf"
    token = os.environ.get("GITHUB_TOKEN") 

    if repo and token:
        create_github_issue(repo, body, token)
    else:
        print("GitHub repository or token not set in environment variables.")

if __name__ == "__main__":
    main()
