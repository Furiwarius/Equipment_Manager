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