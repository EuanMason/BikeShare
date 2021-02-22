function login() {
   var userid = document.querySelector("#userid").value;
   var password = document.querySelector("#password").value;
  $.ajax({
   type:"POST",
   dataType:"json",
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
  $.ajax({
    type: "POST",
    dataType: "json",
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

function bikeIDStartSubmit(value) {
  var bikeid = value;//document.querySelector("#bikeid").value;
  var xcsrft = $.cookie("csrftoken") //"bV2JXP0TnIbUX5Mmq0iF4lUfC34ctY5uZwOKGnaeLwFV8I8lP7OPYLBrLTFcHLKT"; // should get this from cookes
  console.log(xcsrft)
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/rent_bike/",
    async:false,
    data: {
      bikeid: bikeid,
    },
    beforeSend: function (request) {
      request.setRequestHeader("X-CSRFToken", xcsrft);
      console.log(request)
      if (bikeid == "" || bikeid == "") {
        alert("The bikeID cannot be empty");
        return false;
      }
      return true;
    },
    success: function(response){
        if(response.state==2){
          location.href="/start_rent_bike/"+ response.trip_id + "/";
        }
        else if(response.state==0){
          alert("Please input correct BikeID!");
        }
        else if(response.state==1){
          alert("This Bike cannot be used now!");
        }
    },
  });
}

//// Start: Report Bike ////

function CallModal(value) {
  var bikeid = value;//document.querySelector("#bikeid").value;
  if (bikeid == "" || bikeid == "") {
      alert("The bikeID cannot be empty");
      return false;
  } else {
      $('#ReportModal').modal('show');
      $("#bike-report-text").text("Would you like to report a problem with Bike No."+bikeid+"?")
      window.currentBike = bikeid

  };
};

function HideModal() {
  var $modal = $('#ReportModal');
  $modal.modal("hide");
  $modal.on("hidden.bs.modal", function() {
      alert("Success! - This report has been sent to us.");
  });
  /*$modal.on('click', '#ConfirmReport', function(e) {
  });*/
};

function bikeIDErrorSubmit() {
    var xcsrft = $.cookie("csrftoken") //"bV2JXP0TnIbUX5Mmq0iF4lUfC34ctY5uZwOKGnaeLwFV8I8lP7OPYLBrLTFcHLKT"; // should get this from cookes
    var bikeid = window.currentBike  //document.querySelector("#bikeid").value;
    var comment = $("#report-problem").val()
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/report_defective/",
        data: {
            bikeid: bikeid,
            comment: comment
        },
        beforeSend: function(request) {
          request.setRequestHeader("X-CSRFToken", xcsrft);
          if (bikeid == "" || bikeid == "") {
              alert("The bikeID cannot be empty");
              return false;
          }
          return true;
        },
        success: function(response) {
            // alert(response.state)
            HideModal();
            showMap();
        },
    });
}

//// End: Report Bike ////

function getBikes() {
  $.ajax({
    type: "GET",
    dataType: "json",
    url: "/all-bikes/",
    data: {},
    success: function (response) {
      console.log(response);
      var arrayData = response.data;
      var testElement = arrayData[1];
      var stringHtml = `<label className="form-item" for="bike-select">Select a bike</label>
               <select
                  class="form-item"
                  name="bikes"
                  id="bike-select"
                >
                `;
      for (var i = 0; i < arrayData.length; i++) {
        var currentElement = arrayData[i];
        stringHtml += `<option value="${currentElement.bike_id}">${currentElement.bike_id}</option>`;
      }
      $("div#selectBike").html(stringHtml);
      stringHtml += `</select>`
    },
  });
}

// time clock
var GetSeconds=0;
var time=null;
function StartCount(){
	 time=setInterval("count()",1000);
}

function count(){
	hours = Math.floor(GetSeconds/3600);
	mins = Math.floor(GetSeconds/60)%60;
	secs = GetSeconds%60
	$("#time p").html(hours+":"+ mins+":"+ secs);
	GetSeconds++;
	console.info(time);
}
function StopCount(){
	clearInterval(time);
}
