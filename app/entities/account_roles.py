from dataclasses import dataclass


@dataclass
class Roles():
    '''
    Роли аккаунтов в фирмах
    '''

    id: int = None
    # id фирмы, к которой имеет доступ аккаунт
    firm_id: int = None
    # id аккаунта, который имеет доступ к фирме
    account_id: int = None
    # роль аккаунта (super_admin, admin, visitor)
    role: str = None