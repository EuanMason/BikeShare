class User {
  constructor(username, email, password) {
    this.username = username;
    this.email = email;
    this.password = password;
  }
}

// Event Listener
document.querySelector("#user-form").addEventListener("submit", function (e) {
  // Get Form Values
  const username = document.querySelector("#username").value,
        email = document.querySelector("#email").value;
        password = document.querySelector("#password").value;

  const user = new User(username, email, password);
  // console.log(user);

  e.preventDefault();
});