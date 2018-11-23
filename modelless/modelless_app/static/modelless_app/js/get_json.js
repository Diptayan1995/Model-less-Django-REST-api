function get_json() {

  var g_json = {}; //document.getElementById("g_json").value;
  g_json["name"] = document.getElementById("uname").value;
  g_json["password"] = document.getElementById("pword").value;
  g_json["email"] = document.getElementById("email").value;
  g_json['phone'] = document.getElementById("phone").value;


   alert(JSON.stringify(g_json));

         $.ajax({
                    url: "http://localhost:8000/",
                    type: "POST",
                    dataType : 'json',
                    async: false,
                    data: {
                            'query': JSON.stringify(g_json),
                          },
                    success: function (ret) {
                        alert(JSON.stringify(ret));

                    },
                     failure: function() {alert("Error!");},
                    });
}

function login(){

   var cred = {}
   cred["username"] = document.getElementById("username").value;
   cred["password"] =document.getElementById("password").value;
   alert(JSON.stringify(cred));
      $.ajax({
                    url: "http://localhost:8000/login/",
                    type: "POST",
                    dataType : 'json',
                    async: false,
                    data: {
                            'credentials': JSON.stringify(cred),
                          },
                    success: function (data) {
                            alert("HII");
                            alert(JSON.stringify(data["status"]));
                            alert(JSON.stringify(data["url"]));


                             document.cookie = "jwt="+JSON.stringify(data["token"])+";path=/;";

                            window.location.href = data["url"];
                    },
                     failure: function() {alert("Error!");},
                    });
}

function logout(){

         window.location.href = "http://127.0.0.1:8000/logout";

}
