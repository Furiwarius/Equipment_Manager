from app.entities.tool import Tool
from app.entities.worker import Worker as Work
from app.entities.construction import Construction as Constr
from app.entities.storage import Storage as Stor
from app.database.tables.essence import ConstructionTable as ConstrT
from app.database.tables.essence import WorkerTable as WorkT
from app.database.tables.essence import ToolTable as ToolT
from app.database.tables.essence import StorageTable as StorT
from app.database.tables.essence import AccountTable as AccT
from app.entities.account import Account as Acc



class Converter():
    '''
    Конвертиртер

    Переводит данные из классов таблиц
    в классы с голыми данными для слоя бизнес-логики
    '''    

    compliance = {"AccountTable": Acc, 
                  "ConstructionTable": Constr,
                  "WorkerTable": Work,
                  "ToolTable": Tool,
                  "StorageTable": Stor,
                  "Account": AccT,
                  "Construction": ConstrT,
                  "Worker": WorkT,
                  "Tool": ToolT,
                  "Storage": StorT}

    
    def conversion_to_data(self, item:AccT|ConstrT|StorT|WorkT|ToolT) -> Acc|Constr|Stor|Work|Tool: 
        ''' 
        Конвертация из объекта Table
        в объект бизнес логики с 
        голыми данными 
        ''' 
        # Получаем класс бизнес логики соответствующий переданному классу из таблицы
        class_ = self.compliance.get(item.__class__.__name__)
        
        # Получаем атрибуты класса бизнес логики
        param_names = list(class_.__init__.__code__.co_varnames[:class_.__init__.__code__.co_argcount])[1:] 
        
        # Инициализируется с полями None по умолчанию
        result = class_()

        # Заполнение полей
        for atr in param_names:
            setattr(result, atr, getattr(item, atr))
        
        return result 



    def conversion_to_table(self, item:Acc|Constr|Work|Tool|Stor) -> AccT|ConstrT|WorkT|ToolT|StorT:
        '''
        Конвертация из объекта 
        базнес логики с голыми
        данными в объект Table
        '''
        # Получаем атрибуты передаваемого класса
        param_names = list(item.__init__.__code__.co_varnames[:item.__init__.__code__.co_argcount])[1:] 

        # Создаем класс таблицы соответствующий классу бизнес логики
        result = self.compliance.get(item.__class__.__name__)()

        # Заполняем поля
        for atr in param_names:
            setattr(result, atr, getattr(item, atr))

        return result

        