from tool import Tool
from construction import Construction
from worker import Worker
from my_exception import checking_incoming_objects, checking_class, MethodError


class ToolManager():
    '''
    Менеджер инструмента
    '''

    def __init__(self, tool: Tool) -> None:

        # Проверка передаваемых значений
        checking_incoming_objects(self.__init__.__annotations__, [tool])

        self.tool = tool


    def filling_fields (self, construction:Construction) -> None:
        '''
        Первоначальное заполненние полей инструмента.
        Другие методы по измененнию полей и зависимостей
        не будут работать до вызова этого метода
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.filling_fields.__annotations__, [construction])
        
        self.tool.change_construction(construction)

        # Добавление этого инструмента на объект
        construction.add_tool(self.tool)


class WorkerManager():
    '''
    Менеджер работников
    '''

    def __init__(self, worker: Worker) -> None:

        # Проверка передаваемых значений
        checking_incoming_objects(self.__init__.__annotations__, [worker])
        self.worker = worker


    def set_construction(self, construction:Construction) -> None:
        '''
        Присвоение работнику зоны ответственности. Первоначальная настройка.
        При вызове этого метода у работника не должно быть объекта строительства,
        и у объекта строительства также не должно быть ответственного.
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.set_construction.__annotations__, [construction])

        if self.worker.get_construction()==None:
            # Объект строительства добавляется к работнику
            self.worker.change_construction(construction)
            # Смена ответственного лица у объекта строительства
            construction.change_responsible(self.worker)
        else:
            raise MethodError("У этого работника есть закрепленный за ним объект. Используйте метод employee_relocation")



class ConstructionManager():
    '''
    Менеджер объектов
    '''

    def __init__(self, construction: Construction) -> None:
        
        # Проверка передаваемых значений
        checking_incoming_objects(self.__init__.__annotations__, [construction])

        self.construction = construction



    def moving_tool_from_object(self, tools:list, new_construction:Construction) -> None:
        '''
        Перемещение инструмента с текущего объекта на другой объект
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.moving_tool_from_object.__annotations__, [tools, new_construction])

        if self.construction.tool_check(tools):
            self.construction.delete_tools(tools)
            new_construction.add_tools(tools)
            for tool in tools:
                tool.change_construction(new_construction)
        else:
            raise AttributeError("Не все перемещаемые инструменты находятся на текущем объекте")


    def removing_tool(self, tool:Tool) -> None:
        '''
        Удаление инструмента
        '''
        # Проверка передаваемых значений
        checking_class(self.removing_tool.__annotations__, [tool])

        if self.construction.tool_check([tool]):
            self.construction.delete_tool(tool)

        
    def replace_person_responsible(self, new_responsible:Worker) -> None:
        '''
        Заменить ответственного лицо. 
        У нового ответственного не должно быть закрепленного объекта.
        '''

        # Проверка передаваемых значений
        checking_incoming_objects(self.replace_person_responsible.__annotations__, [new_responsible])

        if new_responsible.get_construction()!=None:
            raise MethodError("У нового ответственного есть закрепленный за ним объект")
        
        # Очищаем поле с объектом у текущего ответственного
        self.construction.get_responsible().delete_construction()
        # Добавляем нового ответственного на объект
        self.construction.change_responsible(new_responsible)
        # Заполняем новому ответственному поле с объектом
        new_responsible.change_construction(self.construction)
    

    def close_object(self, tool_storage_location:Construction) -> None:
        '''
        Закрыть объект
        '''
        # Проверка передаваемых значений
        checking_incoming_objects(self.close_object.__annotations__, [tool_storage_location])
        
        # Получение списка инструменов у текущего объекта
        tools = self.construction.get_tools()
        # Переача инструментов новому объекту
        for tool in tools:
            tool.change_construction(tool_storage_location)
        tool_storage_location.add_tools(tools)
        # Удаление инструментов у текущего объекта
        self.construction.delete_tools(tools)
        self.construction.close_construction()
