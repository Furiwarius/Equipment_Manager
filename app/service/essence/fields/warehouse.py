from dataclasses import dataclass
from app.service.essence.fields.tool import Tool

@dataclass
class Storage():
    '''
    Склад
    '''

    id: int
    # название склада
    name: str

    # список инструментов
    tools: dict


    def get_tools(self) -> dict:
        '''
        Получить список инструментов со склада
        '''
        return self.tools
    
    def get_id(self) -> int:
        '''
        Получить id склада
        '''
        return self.id


    def add_tool(self, tool: Tool) -> None:
        '''
        Добавить инструмент на склад
        '''
        self.tools[tool.get_id()] = tool
    

    def delete_tool(self, tool: Tool) -> None:
        '''
        Удалить инструмент со склада
        '''
        self.tools.pop(tool.get_id())
