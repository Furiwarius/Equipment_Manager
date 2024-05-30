import hashlib

def to_hash(data:str) -> str:
    '''
    Перевод строки в hash по алгоритму sha256
    '''
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data.encode())
    return sha256_hash.hexdigest()