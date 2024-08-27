function start_app() {
  const rootNode = document.getElementById("app"); // элемент для рендеринга приложения React
  // получаем корневой элемент 
  const root = ReactDOM.createRoot(rootNode);
  // рендеринг в корневой элемент
  root.render( /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", null, "\u0414\u043E\u0431\u0440\u043E \u043F\u043E\u0436\u0430\u043B\u043E\u0432\u0430\u0442\u044C \u043D\u0430 \u0441\u0435\u0440\u0432\u0438\u0441 EquipmentManager"), /*#__PURE__*/React.createElement("button", {
    onClick: autorization
  }, "\u041D\u0430\u0447\u0430\u0442\u044C")));
}
function autorization() {
  const rootNode = document.getElementById("app"); // элемент для рендеринга приложения React
  // получаем корневой элемент 
  const root = ReactDOM.createRoot(rootNode);
  // рендеринг в корневой элемент
  root.render( /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("h1", null, "\u0414\u043E\u0431\u0440\u043E \u043F\u043E\u0436\u0430\u043B\u043E\u0432\u0430\u0442\u044C \u043D\u0430 \u0441\u0435\u0440\u0432\u0438\u0441 EquipmentManager"), /*#__PURE__*/React.createElement("button", {
    onClick: start_app
  }, "\u041D\u0430\u0437\u0430\u0434"), /*#__PURE__*/React.createElement("p", null, "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043B\u043E\u0433\u0438\u043D: ", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("input", {
    name: "login",
    id: "login"
  })), /*#__PURE__*/React.createElement("p", null, "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043F\u0430\u0440\u043E\u043B\u044C: ", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("input", {
    name: "password",
    id: "password"
  })), /*#__PURE__*/React.createElement("button", {
    onClick: send_user
  }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C"), /*#__PURE__*/React.createElement("p", null, "\u0415\u0441\u043B\u0438 \u043D\u0435\u0442 \u0430\u043A\u043A\u0430\u0443\u043D\u0442\u0430, \u0442\u043E "), /*#__PURE__*/React.createElement("button", {
    onClick: registr
  }, "\u0437\u0430\u0440\u0435\u0433\u0438\u0441\u0442\u0440\u0438\u0440\u0443\u0439\u0442\u0435\u0441\u044C")));
}
function registr() {
  const rootNode = document.getElementById("app"); // элемент для рендеринга приложения React
  // получаем корневой элемент 
  const root = ReactDOM.createRoot(rootNode);
  // рендеринг в корневой элемент
  root.render( /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    id: "registr_form"
  }, /*#__PURE__*/React.createElement("h1", null, "\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044F \u043D\u0430 \u0441\u0435\u0440\u0432\u0438\u0441\u0435 EquipmentManager"), /*#__PURE__*/React.createElement("button", {
    onClick: autorization
  }, "\u041D\u0430\u0437\u0430\u0434"), /*#__PURE__*/React.createElement("p", null, "\u041F\u0440\u0438\u0434\u0443\u043C\u0430\u0439\u0442\u0435 \u043B\u043E\u0433\u0438\u043D: ", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("input", {
    name: "login",
    id: "login"
  })), /*#__PURE__*/React.createElement("p", null, "\u041F\u0440\u0438\u0434\u0443\u043C\u0430\u0439\u0442\u0435 \u043F\u0430\u0440\u043E\u043B\u044C: ", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("input", {
    name: "password",
    id: "password"
  })), /*#__PURE__*/React.createElement("p", null, "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u0432\u0430\u0448\u0443 \u043F\u043E\u0447\u0442\u0443:", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("input", {
    name: "email",
    id: "email"
  })), /*#__PURE__*/React.createElement("button", {
    onClick: send_new_user
  }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C")), /*#__PURE__*/React.createElement("div", {
    id: "code_form",
    style: {
      display: "none"
    }
  }, /*#__PURE__*/React.createElement("h1", null, "\u0420\u0435\u0433\u0438\u0441\u0442\u0440\u0430\u0446\u0438\u044F \u043D\u0430 \u0441\u0435\u0440\u0432\u0438\u0441\u0435 EquipmentManager"), /*#__PURE__*/React.createElement("p", null, "\u0412\u0432\u0435\u0434\u0438\u0442\u0435 \u043A\u043E\u0434 \u043E\u0442\u043F\u0440\u0430\u0432\u043B\u0435\u043D\u043D\u044B\u0439 \u043D\u0430 \u0443\u043A\u0430\u0437\u0430\u043D\u043D\u0443\u044E \u0412\u0430\u043C\u0438 \u043F\u043E\u0447\u0442\u0443:", /*#__PURE__*/React.createElement("br", null), /*#__PURE__*/React.createElement("input", {
    name: "code",
    id: "code",
    placeholder: "00000",
    oninput: "this.value = this.value.slice(0, 5)"
  })), /*#__PURE__*/React.createElement("button", {
    onClick: send_verification_code
  }, "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u043A\u043E\u0434"))));
}
async function send_user() {
  // получаем введеные данные
  const login = document.getElementById("login").value;
  const password = document.getElementById("password").value;

  // отправляем запрос
  const response = await fetch("/login", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      login: login,
      password: password
    })
  });
  if (response.ok) {
    const data = await response.json();
    // Сохранение токена
    localStorage.setItem('authToken', data.token);
    private_office();
  } else {
    alert("Неправильный логин или пароль!");
  }
}
async function send_new_user() {
  await get_verification_code();
  await add_code_form();
}
async function get_verification_code() {
  const email = document.getElementById("email").value;
  const response = await fetch("/confirmation_code", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: email
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
  registr_form.setAttribute("style", "display:none");
  const code_form = document.getElementById("code_form");
  code_form.removeAttribute("style");
}
async function invalid_code() {
  alert("Неправильный код!");
}
async function send_verification_code() {
  const code = document.getElementById("code").value;
  const code_token = sessionStorage.getItem('codeToken');
  const response = await fetch("/check_confirmation_code", {
    method: "POST",
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      code: code,
      jwt: code_token
    })
  });
  if (response.ok) {
    // Удаляем токен с кодом подтверждения, тк проверка уже прошла
    sessionStorage.removeItem('codeToken');
    await send_user_datas();
    autorization();
  } else {
    invalid_code();
  }
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
    headers: {
      "Accept": "application/json",
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      login: login,
      password: password,
      email: email,
      timezone: clientTimeZone
    })
  });
}
start_app();
