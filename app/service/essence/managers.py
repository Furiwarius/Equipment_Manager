from dataclasses import dataclass
from app.service.essence.fields.tool import Tool 
from app.service.essence.fields.worker import Worker 
from app.service.essence.fields.construction import Construction
from app.service.essence.fields.belonging import Belonging
from app.service.essence.fields.warehouse import Storage


@dataclass
class Storekeeper():
    '''
    Кладовщик

    Класс, который занимается организацией
    '''

    # id аккаунта к которому будет 
    # прикреплена информация в таблице belonging
    user_id: int
    # Хранение взаимосвязей
    belonging:list
    # Инструменты
    tools: list
    # Работники
    workers: list
    
    # Отличие объектов от складов в плане хранения
    # в том, что на склады можно перемещать сломанный инструмент
    # Объекты
    constructions: list
    # Склады
    storages: list


    def add_tool(self, new_tool:Tool, storage:Storage, worker:Worker) -> None:
        '''
        Добавление нового инструмента на склад
        '''
        # если этот инструмент еще не добавлен, и работник и склад есть в списках
        if worker in self.workers and storage in self.storages and new_tool not in self.tools:

            self.tools.append(new_tool)
            
            new_belonging = Belonging(user_id=self.user_id,
                                                construction_id=storage.id,
                                                worker_id=worker.id)
            self.belonging.append(new_belonging)


    def move_tool(self, tool:Tool, where) -> None:
        '''
        Перемещение инструмента

        tool - перемещаемый инструмент
        where - новое место (Construction или Storage)
        '''
        if tool in self.tools and where in self.storages or where in self.constructions:
            if isinstance(where, Construction) and where:
                pass

    

    def delete_tool(self, tool: Tool) -> None:
        '''
        Удаление инструмента
        '''
        if tool in self.tools:
            pass

    
    def add_construction(self, new_construction:Construction) -> None:
        '''
        Добавить объект строительства
        '''
        if new_construction not in self.constructions:
            self.constructions.append(new_construction)
        
    
    def add_storage(self, new_storage:Storage) -> None:
        '''
        Добавить склад
        '''
        if new_storage not in self.storages:
            self.constructions.append(new_storage)

    
    def add_worker(self, new_worker:Worker) -> None:
        '''
        Добавить работника
        '''
        if new_worker not in self.workers:
            self.workers.append(new_worker)