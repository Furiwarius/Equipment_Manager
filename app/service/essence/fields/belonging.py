from dataclasses import dataclass



@dataclass
class Belonging():
    '''
    Взаимосвязи

    Хранит id аккаунта пользователя, 
    и связанные с ним объекты, интрументы и рабочих
    '''

    user_id: int
    construction_id: int
    worker_id: int
    tool_id: int

