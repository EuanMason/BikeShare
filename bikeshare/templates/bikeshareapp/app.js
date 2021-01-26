class User {
  constructor(username, email, phone, pwd) {
    this.username = username;
    this.email = email;
    this.phone = phone;
    this.pwd = pwd;
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
  const username = document.querySelector("#username").value,
    email = document.querySelector("#email").value;
  phone = document.querySelector("#phone").value;
  pwd = document.querySelector("#pwd").value;

  // Initianing a user
  const user = new User(username, email, phone, pwd);
  console.log(user);

  // Initianing UI
  const ui = new UI();

  // Validate
  if (username === "" || email === "" || phone === "" || pwd === "")
    // Error alert
    ui.showAlert("Please fill in all field", "error");
  // alert("Failed");

  e.preventDefault();
});
