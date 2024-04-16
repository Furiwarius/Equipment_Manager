from tool import Tool, ToolStatus
from construction import Сonstruction
from worker import Worker


class ToolManager(Tool):
    
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    
    def turn_construction(self, new_construction:Сonstruction) -> None:
        
        # Всякие валидаторы
        # и взаимосвязанные изменения в других классах
        super().change_construction(new_construction)


    def turn_responsible(self, new_responsible:Worker) -> None:

        # Всякие валидаторы
        # и взаимосвязанные изменения в других классах
        super().change_responsible(new_responsible)