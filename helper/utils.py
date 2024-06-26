import hashlib

def md5HashPy(inputStr):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the bytes of the string
    md5_hash.update(inputStr.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    md5_hex = md5_hash.hexdigest()
    return md5_hex