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
  alert(postcode);
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

function bikeIDStartSubmit() {
  var bikeid = document.querySelector("#bikeid").value;
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/home/rent_bike/",
    async:false,
    data: {
      bikeid: bikeid,
    },
    beforeSend: function () {
      if (bikeid == "" || bikeid == "") {
        alert("The bikeID cannot be empty");
        return false;
      }
      return true;
    },
    success: function(response){
        if(response.state==2){
          location.href="rent_bike/start_rent_bike/"+ response.trip_id + "/";
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

function bikeIDErrorSubmit() {
    var bikeid = document.querySelector("#bikeid").value;
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/home/report_defective",
        data: {
            bikeid: bikeid,
        },
        beforeSend: function() {
            if (bikeid == "" || bikeid == "") {
                alert("The bikeID cannot be empty");
                return false;
            }
            return true;
        },
        success: function() {
            //alert(response.state)
            HideModal();
        },
    });
}

function CallModal() {
    var bikeid = document.querySelector("#bikeid").value;
    if (bikeid == "" || bikeid == "") {
        alert("The bikeID cannot be empty");
        return false;
    } else {
        $('#ReportModal').modal('show');
    };
};

function HideModal() {
    var $modal = $('#ReportModal');
    $modal.on('click', '#ConfirmReport', function(e) {
        $modal.modal("hide");
        $modal.on("hidden.bs.modal", function() {
            alert("Success! - This report has been sent to us.");
        });
    });
};

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
