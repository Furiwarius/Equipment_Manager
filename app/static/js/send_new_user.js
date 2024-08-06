async function send_new_user(){
 
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