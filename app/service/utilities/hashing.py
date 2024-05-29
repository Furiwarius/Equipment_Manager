"""
Сервисы это бизнез-логика
Утилиты, это просто мини-программы. Они используются отдельно от БЛ
Можно их и тут оставить, но лучше сделать для них отдельный модуль:
    app/utils/__init__.py
В целом не критично
"""
import hashlib

def to_hash(data:str) -> str:
    '''
    Перевод строки в hash по алгоритму sha256
    '''
    sha256_hash = hashlib.new('sha256')
    sha256_hash.update(data.encode())
    return sha256_hash.hexdigest()
