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
    registr_form.setAttribute("style", "display:none;")
 
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
        window.location.href = '/authorization';
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