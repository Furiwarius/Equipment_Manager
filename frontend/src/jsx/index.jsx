function start_app(){
    const rootNode = document.getElementById("app");    // элемент для рендеринга приложения React
    // получаем корневой элемент 
    const root = ReactDOM.createRoot(rootNode);
    // рендеринг в корневой элемент
    root.render(
        //<h1>Добро пожаловать на сервис EquipmentManager</h1>
        <div>
            <h1>Добро пожаловать на сервис EquipmentManager</h1>
            <a href="/autorization">Начать</a>

        </div>
    );
}

start_app()