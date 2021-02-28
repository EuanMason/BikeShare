/**
 * This file contains the general logic to be executed on the frontend 
 */




/**
 * Calls the API to start renting a bike
 * @param {JQuery|HTMLElement} value - The bike to be rented
 * @param {JQuery|Cookie} xcsrft -  The cookie
 */
function bikeIDStartSubmit(value) {
  // Save the bike and token
  var bikeid = value;
  var xcsrft = $.cookie("csrftoken") 
  
  // Make a REST request using POST protocol to API to start renting a bike
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/rent_bike/",
    async: false,
    data: {
      // Add the bike id as part of the request
      bikeid: bikeid,
    },
    beforeSend: function (request) {
      // Set the CSRF token before send since Django expected that way
      request.setRequestHeader("X-CSRFToken", xcsrft);
      if (bikeid == "" || bikeid == "") {
        alert("The bikeID cannot be empty");
        return false;
      }
      return true;
    },
    success: function (response) {
      // If the API responds 2 go to the renting view
      if (response.state == 2) {
        location.href = "/start_rent_bike/" + response.trip_id + "/";
      }
      // If not, alert of possible errors
      else if (response.state == 0) {
        alert("Please input correct BikeID!");
      }
      else if (response.state == 1) {
        alert("This Bike cannot be used now!");
      }
    },
  });
}

/**
 * Shows the modal to report a problem with the bike
 * @param {JQuery|HTMLElement} value - The bike to be reported
 */
function CallModal(value) {
  // Save bike id on a local variable
  var bikeid = value;
  // Check if is empty then alert an error
  if (bikeid == "" || bikeid == "") {
    alert("The bikeID cannot be empty");
    return false;
  } else {
    // Show modal
    $('#ReportModal').modal('show');
    $("#bike-report-text").text("Would you like to report a problem with Bike No." + bikeid + "?")
    // Set window variable
    window.currentBike = bikeid
  };
};

/**
 * Hides the report a bike modal
 * @param {JQuery|Cookie} modal -  The modal to be hidden
 */
function HideModal() {
  // Get the report modal
  var $modal = $('#ReportModal');
  $modal.modal("hide");
  $modal.on("hidden.bs.modal", function () {
    // When the modal is hide show an alert 
    alert("Success! - This report has been sent to us.");
  });
};

/**
 * Submits the report of a defective bike 
 * @param {JQuery|Cookie} xcsrft -  The cookie
 * @param {WindowElement} bikeid -  The id of defective bike
 * @param {JQuery|HTMLElement} comment -  The comment of the defectiveness
 */
function bikeIDErrorSubmit() {
  
  // Get the values of the cookie, bike and comment
  var xcsrft = $.cookie("csrftoken") 
  var bikeid = window.currentBike  
  var comment = $("#report-problem").val()

  // Make REST request using POST protocol to report the defective of a bike
  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/report_defective/",
    data: {
      bikeid: bikeid,
      comment: comment
    },
    beforeSend: function (request) {
      // Set the CSRF token before send since Django expected that way
      request.setRequestHeader("X-CSRFToken", xcsrft);
      if (bikeid == "" || bikeid == "") {
        alert("The bikeID cannot be empty");
        return false;
      }
      return true;
    },
    success: function (response) {
      // If the API does its job, hide the modal and refresh the map
      HideModal();
      showMap();
    },
  });
}

//// End: Report Bike ////
// no in customer
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
// no in customer
var GetSeconds = 0;
var time = null;
function StartCount() {
  time = setInterval("count()", 1000);
}

// no in customer
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


// no in customer
function count() {
  hours = Math.floor(GetSeconds / 3600);
  mins = Math.floor(GetSeconds / 60) % 60;
  secs = GetSeconds % 60
  $("#time p").html(hours + ":" + mins + ":" + secs);
  GetSeconds++;
  console.info(time);
}
function StopCount() {
  clearInterval(time);
}
