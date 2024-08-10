import secrets

def format_name(str):
    return ' '.join(str.strip().split()).title()

def generate_nonce():
    return secrets.token_urlsafe(16)
