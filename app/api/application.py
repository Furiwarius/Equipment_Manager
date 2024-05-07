from flask import Flask, Blueprint


class Application():
    '''
    Приложение
    '''

    def __init__(self) -> None:
        self.app = Flask(__name__, 
                         static_folder='app/api/static', 
                         template_folder='app/api/templates')
    

    def add_routes(self, bp:Blueprint):
        '''
        Добавить схему blueprint
        '''
        self.app.register_blueprint(bp)


    def run_application(self, debug:bool):
        '''
        Запустить приожение
        '''
        self.app.run(debug=debug)