const http = require("http");
const fs = require("fs");
   
http.createServer(function(request, response){
    
    let filePath = "public/index.html";
    
    switch (request.url) {

        case "/":

            fs.readFile(filePath, function(error, data){
                if(error){
                   
                    response.statusCode = 404;
                    response.end("Resourse not found!");
                }   
                else{
                    response.end(data);
                }
            });
            break;
        
        
        case "/login":
            console.log(response.data)
            break;

        
        case "/registr":
            break;
        
        case "/confirmation_code":
            break;

        case "/check_confirmation_code":
            break;

        default:
            response.statusCode = 404;
            response.end("Resourse not found!");
            break;
    }

}).listen(3000, function(){
    console.log("Server started at http://localhost:3000");
});