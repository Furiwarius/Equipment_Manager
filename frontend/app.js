const http = require("http");
const fs = require("fs");
   
http.createServer(function(request, response){
       
    let filePath = "public/index.html";
    if(request.url !== "/"){
        // получаем путь после слеша
        filePath = request.url.substring(1);
    }
    fs.readFile(filePath, function(error, data){
               
        if(error){
                   
            response.statusCode = 404;
            response.end("Resourse not found!");
        }   
        else{
            response.end(data);
        }
    });
     
}).listen(3000, function(){
    console.log("Server started at http://localhost:3000");
});