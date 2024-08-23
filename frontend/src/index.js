function start_app() {
  const rootNode = document.getElementById("app"); // элемент для рендеринга приложения React
  // получаем корневой элемент 
  const root = ReactDOM.createRoot(rootNode);
  // рендеринг в корневой элемент
  root.render(
  /*#__PURE__*/
  //<h1>Добро пожаловать на сервис EquipmentManager</h1>
  React.createElement("div", null, /*#__PURE__*/React.createElement("h1", null, "\u0414\u043E\u0431\u0440\u043E \u043F\u043E\u0436\u0430\u043B\u043E\u0432\u0430\u0442\u044C \u043D\u0430 \u0441\u0435\u0440\u0432\u0438\u0441 EquipmentManager"), /*#__PURE__*/React.createElement("a", {
    href: "/autorization"
  }, "\u041D\u0430\u0447\u0430\u0442\u044C")));
}
start_app();
