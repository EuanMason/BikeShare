function login() {
   var userid = document.querySelector("#userid").value;
   var password = document.querySelector("#password").value;
  $.ajax({
   type:"POST",
   dataType:'json',
   url:"/login/",
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

function postCodeSubmit() {
  var postcode = document.querySelector("#postcode").value;
  alert(postcode);
  $.ajax({
    type: "POST",
    dataType: json,
    url: "/bike/postcode",
    data: {
      postcode: postcode,
    },
    beforeSend: function () {
      if (postcode == "" || postcode == "") {
        alert("The postcode cannot be empty");
        return false;
      }
      return true;
    },
  });
}

function bikeIDStartSubmit() {
  var bikeID = document.querySelector("#bikeID").value;
  alert(bikeID);
  $.ajax({
    type: "POST",
    dataType: json,
    url: "/bike/bikeID",
    data: {
      bikeID: bikeID,
    },
    beforeSend: function () {
      if (bikeID == "" || bikeID == "") {
        alert("The bikeID cannot be empty");
        return false;
      }
      return true;
    },
  });
}

function bikeIDErrorSubmit() {
  var bikeID = document.querySelector("#bikeID").value;
  alert(bikeID);
  $.ajax({
    type: "POST",
    dataType: json,
    url: "/bike/bikeID",
    data: {
      bikeID: bikeID,
    },
    beforeSend: function () {
      if (bikeID == "" || bikeID == "") {
        alert("The bikeID cannot be empty");
        return false;
      }
      return true;
    },
  });
}


