import secrets

def flag():
    return f"flag{{{secrets.token_hex(16)}}}"

print(flag())