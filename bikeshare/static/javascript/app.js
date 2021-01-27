class User {
  constructor(userid, email, phone, password) {
    this.userid = userid;
    this.email = email;
    this.phone = phone;
    this.password = password;
  }
}

class UI {
  showAlert(message, className) {
    // Create a div
    const div = document.createElement("div");
    div.className = `alert ${className}`;
    // Add Text
    // div.textContent = message;
    div.appendChild(document.createTextNode(message));

    // Get Form
    const form = document.querySelector("#user-form");
    // Get Parent
    const container = document.querySelector(".container");
    //Insert Alert
    container.insertBefore(div, form);

    // Disapear after 3s
    setTimeout(function () {
      document.getElementsByClassName(className)[0].remove();
    }, 2000);
  }
}

// Local Storage class
class Store {
  static getUsers() {
    let users;
    if (localStorage.getItem("users") === null) {
      users = [];
    } else {
      users = JSON.parse(localStorage.getItem("users"));
    }

    return users;
  }
}

// Event Listhers
// DOM Load event
document.addEventListener("DOMContentLoaded", Store.displayBooks);

// Event Listener for add a book
document.querySelector("#user-form").addEventListener("submit", function (e) {
  // Get Form Values
  const userid = document.querySelector("#userid").value,
    email = document.querySelector("#email").value;
  phone = document.querySelector("#phone").value;
  password = document.querySelector("#password").value;

  // Initianing a user
  const user = new User(userid, email, phone, password);
  console.log(user);

  // Initianing UI
  const ui = new UI();

  // Validate
  if (username === "" || email === "" || pwd === "") {
    // Error alert
    ui.showAlert("Please fill in all field", "error");
  }
  else
  {
      document.querySelector("#user-form").submit();
  }
  // alert("Failed");

  e.preventDefault();
});

function login() {
   var userid = document.querySelector("#userid").value;
   var password = document.querySelector("#password").value;
  $.ajax({
   type:"POST",
   dataType:json,
   url:"/login_views/login",
   data:{
    "userid":userid,
    "password":password
   },
   beforeSend : function(){
				if(userid == "" || password == ""){
					alert("The username or password cannot be empty")
					return false;
				}
				return true;
			},
			success: function(data){
				//{"success" : true}
				//{"success" : false , "errorMsg" : "User name or password error!"}
				//{"success" : false , "errorMsg" : "Sorry, your account is invalid"}
				if(data.success){
					//Send get request to jump to the page
					document.location.href = "../index.html";
				}
			}

   })
}

