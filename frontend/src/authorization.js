$('#myDiv').empty(); // очистка содержимого перед выводом данных

const rootNode = document.getElementById("app");    // элемент для рендеринга приложения React
// получаем корневой элемент 
const root = ReactDOM.createRoot(rootNode);
// рендеринг в корневой элемент
root.render(
    <div>
        <h1>Добро пожаловать на сервис EquipmentManager</h1>
        <a href="/">Назад</a>
        
        <p>
            Введите логин: <br /> 
            <input name="login" id="login" />
        </p>
        <p>
            Введите пароль: <br /> 
            <input name="password" id="password"/>
        </p>
        <button onclick="send_user()">Отправить</button>

        <p>Если нет аккаунта, то <a href="/registr">зарегистрируйтесь</a></p>

    </div>
);


async function send_user(){
 
    // получаем введеные данные
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;

    // отправляем запрос
    const response = await fetch("/login", {
                        method: "POST",
                        headers: { "Accept": "application/json", "Content-Type": "application/json" },
                        body: JSON.stringify({ 
                            login: login,
                            password: password
                            })
                        });
    if (response.ok){
        const data = await response.json(); 
        // Сохранение токена
        localStorage.setItem('authToken', data.token);
        private_office()
    }
    else {
        alert("Неправильный логин или пароль!");
    }
}