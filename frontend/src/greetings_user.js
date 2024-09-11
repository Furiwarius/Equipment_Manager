function greetings() {

    var date = new Date();
    
    var hh = date.getHours(); //часы   
    
    if (hh > 23 || hh < 6){
        set_headler("Доброй ночи!")
    } else if (hh => 6 || hh < 10){
        set_headler("Доброе утро!")
    } else if (hh => 10 || hh < 17){
        set_headler("Добрый день!")
    } else {
        set_headler("Добрый вечер!")
    }
    };



function set_headler(value){
    const headler = document.getElementById("greetings")
    headler.textContent = value
}