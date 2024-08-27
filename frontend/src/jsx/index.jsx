function start_app(){
    const rootNode = document.getElementById("app");    // элемент для рендеринга приложения React
    // получаем корневой элемент 
    const root = ReactDOM.createRoot(rootNode);
    // рендеринг в корневой элемент
    root.render(
        <div>
            <h1>Добро пожаловать на сервис EquipmentManager</h1>
            <button onClick={autorization}>Начать</button>

        </div>
    );
}


function autorization() {
    const rootNode = document.getElementById("app");    // элемент для рендеринга приложения React
    // получаем корневой элемент 
    const root = ReactDOM.createRoot(rootNode);
    // рендеринг в корневой элемент
    root.render(
        <div>
            <h1>Добро пожаловать на сервис EquipmentManager</h1>
            <button onClick={start_app}>Назад</button>
            
            <p>
                Введите логин: <br /> 
                <input name="login" id="login" />
            </p>
            <p>
                Введите пароль: <br /> 
                <input name="password" id="password"/>
            </p>
            <button onClick={send_user}>Отправить</button>


            <p>Если нет аккаунта, то </p>
            <button onClick={registr}>зарегистрируйтесь</button>
        </div>
    );
}



function registr() {
    const rootNode = document.getElementById("app");    // элемент для рендеринга приложения React
    // получаем корневой элемент 
    const root = ReactDOM.createRoot(rootNode);
    // рендеринг в корневой элемент
    root.render(
        <div>
            <div id="registr_form">
                <h1>Регистрация на сервисе EquipmentManager</h1>
                <button onClick={autorization}>Назад</button>

                <p>
                    Придумайте логин: <br /> 
                    <input name="login" id="login" />
                </p>
                <p>
                    Придумайте пароль: <br /> 
                    <input name="password" id="password"/>
                </p>
                <p>
                    Введите вашу почту:<br />
                    <input name="email" id="email"/>
                </p>
                <button onClick={send_new_user}>Отправить</button>
            </div>


            <div  id="code_form" style={{display:"none"}}>
                <h1>Регистрация на сервисе EquipmentManager</h1>
                
                <p>
                    Введите код отправленный на указанную Вами почту:<br />
                    <input name="code" id="code" placeholder="00000" oninput="this.value = this.value.slice(0, 5)"/>
                </p>
                <button onClick={send_verification_code}>Отправить код</button>
            </div>
        </div>

    );
}



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



async function send_new_user(){
 
    await get_verification_code()
    await add_code_form()
}



async function get_verification_code() {
    
    const email = document.getElementById("email").value;

    const response = await fetch("/confirmation_code", {
                            method: "POST",
                            headers: { "Accept": "application/json", "Content-Type": "application/json" },
                            body: JSON.stringify({ 
                                email: email,
                                })
                            });
    if (response.ok) {
        const data = await response.json(); 
        // Сохранение токена с проверочным кодом
        sessionStorage.setItem('codeToken', data.code);
    }
}



async function add_code_form() {
    
    const registr_form = document.getElementById("registr_form");
    registr_form.setAttribute("style", "display:none")
 
    const code_form = document.getElementById("code_form");
    code_form.removeAttribute("style")
}



async function invalid_code() {
    alert("Неправильный код!");
}



async function send_verification_code() {

    const code = document.getElementById("code").value;
    const code_token = sessionStorage.getItem('codeToken');

    const response = await fetch("/check_confirmation_code", {
                            method: "POST",
                            headers: { "Accept": "application/json", "Content-Type": "application/json" },
                            body: JSON.stringify({ 
                                code: code,
                                jwt: code_token
                                })
                            });
    if (response.ok) {
        // Удаляем токен с кодом подтверждения, тк проверка уже прошла
        sessionStorage.removeItem('codeToken')
        await send_user_datas()
        autorization()
        }
    else {
        invalid_code()}
} 




async function send_user_datas() {
    // получаем введеные данные
    const login = document.getElementById("login").value;
    const password = document.getElementById("password").value;
    const email = document.getElementById("email").value;
    const clientTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;

    // отправляем запрос
    await fetch("/registr", {
        method: "POST",
        headers: { "Accept": "application/json", "Content-Type": "application/json" },
        body: JSON.stringify({ 
            login: login,
            password: password,
            email: email,
            timezone: clientTimeZone
            })
        });
}



start_app()