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
from app.entities.firm import Firm
from app.database.tables.essence import FirmTable as FirmT
import functools 



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
                  "FirmTable":Firm,
                  "Account": AccT,
                  "Construction": ConstrT,
                  "Worker": WorkT,
                  "Tool": ToolT,
                  "Storage": StorT,
                  "Firm": FirmT}

    
    def conversion_to_data(self, item:AccT|ConstrT|StorT|WorkT|ToolT|FirmT|None) -> Acc|Constr|Stor|Work|Tool|Firm|None: 
        ''' 
        Конвертация из объекта Table
        в объект бизнес логики с 
        голыми данными 
        ''' 
        if item is None:
            return None
        
        # Получаем класс бизнес логики соответствующий переданному классу из таблицы
        class_ = self.compliance.get(item.__class__.__name__)
        
        # Получаем атрибуты класса бизнес логики
        param_names = list(class_.__init__.__code__.co_varnames[:class_.__init__.__code__.co_argcount])[1:] 
        
        # Инициализируется с полями None по умолчанию
        class_instance = class_()

        # Заполнение полей
        for atr in param_names:
            setattr(class_instance, atr, getattr(item, atr))
        
        return class_instance 



    def conversion_to_table(self, item:Acc|Constr|Work|Tool|Stor|Firm) -> AccT|ConstrT|WorkT|ToolT|StorT|FirmT:
        '''
        Конвертация из объекта 
        базнес логики с голыми
        данными в объект Table
        '''
        # Получаем атрибуты передаваемого класса
        param_names = list(item.__init__.__code__.co_varnames[:item.__init__.__code__.co_argcount])[1:] 

        # Создаем класс таблицы соответствующий классу бизнес логики
        class_instance = self.compliance.get(item.__class__.__name__)()

        # Заполняем поля
        for atr in param_names:
            setattr(class_instance, atr, getattr(item, atr))

        return class_instance

        
    
    def conversion_input_args(self, args:tuple) -> tuple:
        '''
        Переводит entities экземпляры в образы таблиц 
        '''

        new_args = list()
        for arg in args:
            if isinstance(arg, (Acc, Constr, Work, Tool, Stor, Firm)):
                new_args.append(self.conversion_to_table(arg))
            else:
                new_args.append(arg)
        
        return new_args



    def conversion_input_kwargs(self, kwargs:dict) -> dict:
        '''
        Переводит entities экземпляры в образы таблиц   
        '''
        new_kwargs = dict()
        for key, item in kwargs.items():
            if isinstance(item, (Acc, Constr, Work, Tool, Stor, Firm)):
                new_kwargs[key] = self.conversion_to_table(item)
            else:
                new_kwargs[key] = item
        return new_kwargs
    


    def conversion_result_func(self, result:list|dict|AccT|ConstrT|WorkT|ToolT|StorT|FirmT):
        
        if isinstance(result, list):
            result = [self.conversion_to_data(item) for item in result]
        
        elif isinstance(result, dict):
            result = {key:self.conversion_to_data(item) for key, item in result.items()}

        elif isinstance(result, (AccT, ConstrT, WorkT, ToolT, StorT, FirmT)):
            result = self.conversion_to_data(result)
        
        return result
    


converter = Converter()



def convertertation(func) -> Acc|Constr|Work|Tool|Stor|Firm|None:
    '''
    Конвертор декоратор

    Переводит входящие даннные в круды к табличным представлениям, 
    а результат к классам entities
    '''
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Acc|Constr|Work|Tool|Stor|Firm|dict|list|None:        
        
        try:
            result = func(*converter.conversion_input_args(args), 
                          **converter.conversion_input_kwargs(kwargs))
        except Exception as er:
            raise er

        return converter.conversion_result_func(result)

    return wrapper