from dataclasses import dataclass
from tool import Tool

@dataclass
class Storage():
    '''
    Склад
    '''

    id: int
    # название склада
    name: str

    # список инструментов
    tools: list


    def get_tools(self) -> list:
        '''
        Получить список инструментов со склада
        '''
        return self.tools


    def add_tool(self, tool: Tool) -> None:
        '''
        Добавить инструмент на склад
        '''
        self.tools.append(tool)
    

    def delete_tool(self, tool: Tool) -> None:
        '''
        Удалить инструмент со склада
        '''
        self.tools.remove(tool)
