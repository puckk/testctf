import random
import os
import requests
from Crypto.Cipher import AES

FLAG = "glovo{this_is_a_fake_flag_for_demo_purposes}"

def generate_random_string(length=16):
    """Generate a random string of fixed length."""
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for _ in range(length))

def blend_key(key_bytes):
    key_int = int(key_bytes.hex(), 16)
    return key_int * random.randint(1, 99999) * random.randint(1, 99999) * random.randint(1, 99999) + 998877665544332211

def create_github_issue(repo, title, body, token):
    url = f"https://api.github.com/repos/{repo}/issues"
    print(f"Creating issue in {repo} with title '{title}'")
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }
    data = {
        "title": title,
        "body": body
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()

def main():
    key = generate_random_string().encode()
    iv = b"product_security"
    cipher = AES.new(key, AES.MODE_OFB, iv)
    encrypted_flag = cipher.encrypt(FLAG.encode())
    shuffled_keys = [str(blend_key(key)) for _ in range(20)]

    body = (
        "Your shuffled keys:\n"
        + "\n".join(shuffled_keys)
        + "\n\nHere's your encrypted flag:\n"
        + encrypted_flag.hex()
    )
    
    print(body)

    # Get repo, token, and issue title from environment variables
    repo = "puckk/testctf"
    token = os.environ.get("GITHUB_TOKEN")  # Set this secret in GitHub Actions
    issue_title = "CTF Challenge Output"

    if repo and token:
        create_github_issue(repo, issue_title, body, token)
    else:
        print("GitHub repository or token not set in environment variables.")

if __name__ == "__main__":
    main()
