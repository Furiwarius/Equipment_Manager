from dataclasses import dataclass
from datetime import datetime
from app.service.essence.fields.tool import Tool, ToolStatus
from app.service.essence.fields.worker import Worker, StatusWorker
from app.service.essence.fields.construction import Construction, ConstructionStatus
from app.service.essence.fields.belonging import Belonging
from app.service.essence.fields.warehouse import Storage


@dataclass
class Storekeeper():
    '''
    Кладовщик

    Класс, который занимается организацией
    '''

    def __init__(self, user_id:int) -> None:
        # id аккаунта к которому будет 
        # прикреплена информация в таблице belonging
        self.user_id = user_id

        # Объекты хранятся в словарях в виде {id:object}
        # Инструменты
        self.tools = dict()
        # Работники
        self.workers = dict()
        # Отличие объектов от складов в плане хранения
        # в том, что на склады можно перемещать сломанный инструмент
        # Объекты
        self.constructions = dict()
        # Склады
        self.storages = dict()


    def filling_data(self) -> None:
        '''
        Метод, заполняющий поля tools, workers и тд,
        данными из базы данных.
        '''


    def get_id_storages(self) -> list:
        '''
        Получение списка id складов
        '''
        return list(self.storages.keys())
    

    def get_storage_by_id(self, id_storage:int) -> Storage:
        '''
        Получение склада по id
        '''
        return self.storages.get(id_storage)
    

    def get_id_tools(self) -> list:
        '''
        Получение списка id инструментов
        '''
        return list(self.tools.keys())
    

    def get_tool_by_id(self, id_tool:int) -> Tool:
        '''
        Получение инструмента по id
        '''
        return self.tools.get(id_tool)


    def get_id_workers(self) -> list:
        '''
        Получение списка id работников
        '''
        return list(self.workers.keys())


    def get_worker_by_id(self, id_worker:int) -> Worker:
        '''
        Получение работника по id
        '''
        return self.workers.get(id_worker)


    def get_id_construction(self) -> list:
        '''
        Получение списка id объектов строительства
        '''
        return list(self.constructions.keys())


    def get_construction_by_id(self, id_constr:int) -> Construction:
        '''
        Получение объекта строительства по id
        '''
        return self.constructions.get(id_constr)


    def add_tool(self, tool:Tool, storage:Storage) -> None:
        '''
        Добавление нового инструмента на склад
        '''
        # если этот инструмент еще не добавлен, и склад есть в списках
        if storage.get_id() in self.get_id_storages() and tool.get_id() not in self.get_id_tools():
            self.tools[tool.get_id()] = tool
            storage.add_tool(tool)
            tool.move_tool(storage.get_id())
            tool.change_date(datetime.now())


    def move_tool(self, tool:Tool, where:Construction) -> None:
        '''
        Перемещение инструмента

        tool - перемещаемый инструмент
        where - новое место (Construction или Storage)
        На Storage можно перемещать нерабочий инструмент.
        '''
        if tool.get_id() in self.tools and where.get_id() in self.storages or where.get_id() in self.constructions:
            condition = tool.get_status()==ToolStatus.works and where.get_status()==ConstructionStatus.works
            if isinstance(where, Construction) and condition and where.get_worker():
                self.__operations_moving_tool(tool, where)
            elif isinstance(where, Storage):
                self.__operations_moving_tool(tool, where)
        else:
            raise AttributeError("Передаваемые атрибуты не добавлены")


    def __operations_moving_tool(self, tool:Tool, where:Storage) -> None:
        '''
        Операции по перемещению инструмента
        '''
        constr_id = tool.get_construction()
        if constr_id in self.get_id_construction():
            self.get_construction_by_id(tool.get_construction()).delete_tool(tool)
        elif constr_id in self.get_id_storages():
            self.get_storage_by_id(tool.get_construction()).delete_tool(tool)
        tool.move_tool(where.get_id())
        tool.change_date(datetime.now())
        where.add_tool(tool)


    def delete_tool(self, tool: Tool) -> None:
        '''
        Удаление инструмента

        Удалить инструмент можно, только 
        если он находится на складе
        '''
        if tool.get_id() in self.tools and tool.get_construction() in self.storages:
            self.storages.get(tool.get_construction()).delete_tool(tool)
            self.tools.pop(tool.get_id())
        else:
            raise AttributeError("Инструмент находится на объекте. Переместите на склад.")


    def add_construction(self, construction:Construction) -> None:
        '''
        Добавить объект строительства
        '''
        if construction.get_id() not in self.constructions:
            self.constructions[construction.get_id()] = construction


    def delete_construction(self, construction:Construction) -> None:
        '''
        Удалить объект строительства
        '''
        if construction.get_id() in self.constructions:
            if not construction.get_tools():
                # Если у объекта нет инструментов, то можем его удалять
                self.constructions.pop(construction.get_id())
                if construction.get_worker():
                    # Если у объекта есть ответственный, то удаляем этот объект у него
                    self.workers.get(construction.get_worker()).change_construction()


    def add_storage(self, storage:Storage) -> None:
        '''
        Добавить склад
        '''
        if storage.get_id() not in self.storages:
            self.storages[storage.get_id()] = storage

    
    def add_worker(self, worker:Worker) -> None:
        '''
        Добавить работника
        '''
        if worker.get_id() not in self.workers:
            self.workers[worker.get_id()] = worker


    def delete_worker(self, worker:Worker) -> None:
        '''
        Удалить работника
        '''
        if worker.get_id() in self.workers:
            if not worker.get_construction():
                raise AttributeError("Работник является ответственным лицом на объекте.")
            else:
                self.workers.pop(worker.get_id())


    def appointment_responsible(self, worker:Worker, construction:Construction) -> None:
        '''
        Назначить ответственного на объект
        '''
        if worker.get_status() is StatusWorker.works and not worker.get_construction():
            # Если работник в состоянии работать, то:
            if construction.get_id() not in self.constructions or worker.get_id() not in self.workers:
                self.add_worker(worker)
                self.add_construction(construction)
            self.__remove_construction(construction)
        
            construction.add_worker(worker)
            worker.change_construction(construction.get_id())
            worker.change_date_work(datetime.now())

    
    def __remove_construction(self, construction:Construction) -> None:
        '''
        Убрать объект у предыдущего работника,
        который отвечает за данных объект
        '''
        if construction.get_worker():
            worker = self.get_worker_by_id(construction.get_worker())
            worker.change_construction()