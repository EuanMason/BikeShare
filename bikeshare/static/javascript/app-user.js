/**
 * This file contains the customer/user logic to be executed user_page.html
 */

// Init basic global variables
let map;
var trip;
let markersList = []

/**
 * Populates the map with the markers and start some basic functionalities
*/
function showInitMap(results) {
    // Hide message of no bikes available
    $("#main-no-bike-available").hide()

    // Make the REST request using a GET protocol to get all the available location with bikes
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/locations-of-availabe-bikes/",
        data: {},
        success: function (response) {
            // Save the response location as an array
            var arrayData = response.location;

            // Iterate over the array to create the locations markers
            for (let i = 0; i < arrayData.length; i++) {

                // Get data to be used
                var currentData = arrayData[i];
                var longitudeData = arrayData[i].longitude;
                var latitudeData = arrayData[i].latitude;

                // Create marker object using Google Maps
                const latLng = new google.maps.LatLng(latitudeData, longitudeData);
                const marker = new google.maps.Marker({
                    position: latLng,
                    map: map,
                    title: "location_id_: " + (currentData.location_id),
                })

                // Create a popup based in a string for that will be called when the marker is clicked
                const contentPopup =
                    '<div id="content">' +
                    '<div id="siteNotice">' +
                    "</div>" +
                    '<h3 id="firstHeading" class="firstHeading">' + currentData.line_1 + '</h3>' +
                    '<div id="bodyContent">' +
                    "<p><b>Postcode:</b> " + currentData.postcode + "</p>" +
                    "<p><b>City:</b> " + currentData.city + "</p>" +
                    "</div>" +
                    "</div>";

                // Create the popup as a Google Maps object
                const infoPopup = new google.maps.InfoWindow({
                    content: contentPopup,
                });

                // Add an click listener to marker
                marker.addListener("click", () => {
                    infoPopup.open(map, marker);
                });
            }
        },
    });
}

/**
 * Redirects to the ongoing trip view
*/
function goToTrip() {
    location.href = "/start_rent_bike/" + trip + "/";
}

/**
 * Update the map when the customer selects a location to look for bikes
 * @param {JQuery|HTMLElement} postcode -  The postcode value on the input
*/
function showMap(results) {
    // Get the postcode valude
    var postcode = $("#postcode").val()
    // Validate the postcode is not empty neither only spaces
    if (postcode.split(' ').join('').length == 0) {
        // In case the input is empty
        //alert("ERROR: Please write a postcode")
        callModalAlert("ERROR", "Please write a postcode")
        // Cut the execution 
        return
    }

    // Remove the spaces in case there are some
    postcode = postcode.replace(' ', '')
    // Check that there is still values after removing the spaces
    if (postcode.length > 0) {
        // Make the REST request using GET protocol to obtain all the bikes in that location
        $.ajax({
            type: "GET",
            dataType: "json",
            url: "/all-bikes-location/" + postcode,
            data: {},
            success: function (response) {
                // hide the text that ask for the postcode at the beginning
                $("#alertInitPostcode").hide();
                // Show the area to select bikes
                $('#ride-bike').show();
                // Clean markers 
                for (let j = 0; j < markersList.length; j++) {
                    markersList[j].setMap(null);
                }
                markersList = []

                // Get the location and bikes from the REST response
                var loc = response.data.loc
                var bikes = response.data.bikes
                // Create latlong object to center the map
                var myLatLong = new google.maps.LatLng(loc.latitude, loc.longitude);
                window.setTimeout(() => {
                    map.panTo(myLatLong);
                    map.setZoom(22);
                    map.setCenter(myLatLong);
                }, 30);

                // Create the image marker
                const image = {
                    url: imgs + '/bike.png',
                    origin: new google.maps.Point(0, 0),
                    scaledSize: new google.maps.Size(60, 60),
                };

                // These are constant to show bike icon on maps
                var pi = Math.PI
                var degrees = 180;
                var radious = 0.00001;
                var randomess_l1 = 0
                var randomess_l2 = 360

                // The html to be added to DOM when iteration finishes
                var stringHtml = '';
                for (let i = 0; i < bikes.length; i++) {
                    // Get the current bike on the iteration
                    var currentBike = bikes[i];

                    // Get the latitude of the bike's location
                    var longitudeData = currentBike.location.longitude;
                    var latitudeData = currentBike.location.latitude;
                    // The way to display the bike markers on the map was based on the following
                    // Mahdi. How to place markers on the outline of a circle in google maps?. 
                    // On: https://gis.stackexchange.com/questions/37615/how-to-place-markers-on-the-outline-of-a-circle-in-google-maps
                    // Accesed on: Feb, 11 2021
                    var randomness_degrees = Math.floor(Math.random() * (randomess_l2 - randomess_l1) + randomess_l1);
                    var longitudeBike = Math.cos(randomness_degrees * pi / 180) * radious + longitudeData;
                    var latitudeBike = Math.sin(randomness_degrees * pi / 180) * radious + latitudeData;

                    // Create a latitude and longitude object to place the bike
                    const latLngBike = new google.maps.LatLng(latitudeBike, longitudeBike);

                    // Set the new bike marker
                    const marker = new google.maps.Marker({
                        position: latLngBike,
                        map: map,
                        title: "bike_: " + (currentBike.bike_id),
                        icon: image, // Add the custom image marker
                        label: {
                            text: "No. " + currentBike.bike_id,
                            color: "#ffffff",
                            fontSize: "20px",
                            fontWeight: "bold"
                        },
                    })
                    // Add the marker to the list
                    markersList.push(marker)

                    // Create a boostrap's grid of 3x3. So it is needed to know if a new row is starting
                    if (i % 3 == 0) {
                        if (i > 0) {
                            stringHtml += '</div>';
                            stringHtml += '<div class="row">';
                        }
                        else if (i == 0) {
                            stringHtml += '<div class="row">';
                        }
                    }

                    // Add a column per bike on the DOM
                    stringHtml += '<div class="col">';
                    stringHtml += '	<div class="row">';
                    stringHtml += '	  <div class="col grid-img-style">';
                    stringHtml += '		<img class="grid-style " src="' + imgs + '/bike.png" alt="bike">';
                    stringHtml += '		<h4>Bike ' + "No. " + currentBike.bike_id + '</h4>';
                    stringHtml += '	  </div>';
                    stringHtml += '	</div>';
                    stringHtml += '	<div class="row">';
                    stringHtml += '	  <div class="col">';
                    stringHtml += '		<button';
                    stringHtml += '		  class="startbox btn btn-primary grid-style"';
                    stringHtml += '		  type="button"';
                    stringHtml += '		  onclick="bikeIDStartSubmit(' + currentBike.bike_id + ')"';
                    stringHtml += '		>';
                    stringHtml += '		  Start';
                    stringHtml += '		</button>';
                    stringHtml += '	  </div>';
                    stringHtml += '	  <div class="col">';
                    stringHtml += '		<!--- Report Button -->';
                    stringHtml += '		<button';
                    stringHtml += '		  class="btn btn-dark grid-style"';
                    stringHtml += '		  onclick="CallModal(' + currentBike.bike_id + ')"';
                    stringHtml += '		>';
                    stringHtml += '		  Report A Problem!';
                    stringHtml += '		</button>';
                    stringHtml += '	  </div>';
                    stringHtml += '	</div>';
                    stringHtml += '</div>';
                }

                // Show message if there is no bike available in the location
                if (bikes.length == 0) {
                    $("#main-no-bike-available").show()
                }
                else {
                    $("#main-no-bike-available").hide()
                }

                // Close the grid depending on the amount of bikes available
                var neededOnGrid = 3 - (bikes.length % 3);
                if ((bikes.length % 3) == 0) {
                    neededOnGrid = 0
                }
                for (let x = 0; x < neededOnGrid; x++) {
                    stringHtml += '<div class="col"></div>';
                }
                stringHtml += '</div>'

                // Add the created string to the DOM as a html object
                $('#main-container-bikes').html(stringHtml);
            },
            error: function (response, textStatus, errorThrown) {
                // In case there is no bike at the location and 404 is returned from the API
                if (response.status == 404) {
                    //alert("There is no bike in this place. Try another one")
                    callModalAlert("ERROR", "There is no bike in this place. Try another one")
                }
            }
        });
    }
}

/**
 * Calls the API to add money to the wallet based on the fields filled by the user
 * @param {JQuery|HTMLElement} amount -  The amount to be added to the user's wallet
 * @param {JQuery|Cookie} xcsrft - the CSRF token on the cookies
*/
function addMoneyWallet() {
    // Get the amount and the token
    var amount = $("#am").val()
    var xcsrft = $.cookie("csrftoken")

    // Get the values of the fields
    var creditNumber = $("#dummy-credit").val()
    var expDate = $("#dummy-date").val()
    var security = $("#dummy-security").val()

    // General boolean to know if the validation passed
    var boolGeneralPass = true
    // Check if the field is empty - Credit card
    if (creditNumber.split(' ').join('').length == 0) {
        callModalAlert("ERROR", "Credit card must be provided")
        boolGeneralPass = boolGeneralPass && false
    }
    // Validate to avoid multiple modals overlap
    if (boolGeneralPass == false) {
        return
    }
    // Check if it is of length 16 and all numbers
    //  Also check if it is a number using JS funciton parseFloat
    var boolCreditCard = creditNumber.length == 16 && parseFloat(creditNumber)
    if (boolCreditCard == false) {
        callModalAlert("ERROR", "Credit card must be 16 lenght and number")
        boolGeneralPass = boolGeneralPass && false
    }
    // Validate to avoid multiple modals overlap
    if (boolGeneralPass == false) {
        return
    }

    // Check if the field is empty - Date 
    if (expDate.split(' ').join('').length == 0) {
        callModalAlert("ERROR", "Expiration date Date card must be provided")
        boolGeneralPass = boolGeneralPass && false
    }
    // Validate to avoid multiple modals overlap
    if (boolGeneralPass == false) {
        return
    }

    // Check if the field is empty - Security code 
    if (security.split(' ').join('').length == 0) {
        callModalAlert("ERROR", "Security code must be provided")
        boolGeneralPass = boolGeneralPass && false
    }
    // Validate to avoid multiple modals overlap
    if (boolGeneralPass == false) {
        return
    }
    // Check if it is of length 16 and all numbers
    //  Also check if it is a number using JS funciton parseFloat
    var boolSecurity = security.length == 3 && parseFloat(security)
    if (boolSecurity == false) {
        callModalAlert("ERROR", "Credit card must be 3 lenght and number")
        boolGeneralPass = boolGeneralPass && false
    }
    // Validate to avoid multiple modals overlap
    if (boolGeneralPass == false) {
        return
    }

    // Check if the field is empty - Amount
    if (amount.split(' ').join('').length == 0) {
        callModalAlert("ERROR", "Amount of money must be provided")
        boolGeneralPass = boolGeneralPass && false
    }
    // Validate to avoid multiple modals overlap
    if (boolGeneralPass == false) {
        return
    }

    // Make the REST requesto to API using a POST protocol to add money to the wallet
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/recalculate-wallet/",
        data: {
            amount: amount
        },
        beforeSend: function (request) {
            // Add the token as part of the header
            // This is needed since Django expects this field for POST requests
            request.setRequestHeader("X-CSRFToken", xcsrft);
        },
        success: function (response) {
            var data = response.data;
            var credit = data.credit
            var text = ""
            // Validate the current amount of money in the wallet after transaction
            if (credit < 0) {
                // If there is still a debt
                text = "You have a debt of £" + (-1 * credit) + ". You will need to add enough money to your wallet before riding again"
                //alert("You have a debt of " + (-1 * credit) + ". You will need to add enough money to your wallet before riding again")
            }
            else {
                // If the user has a superavit (i.e more money that the spedend)
                //alert("Your current credit is " + credit)
                text = "Your current credit is £" + credit
            }
            callModalAlert("INFO", text, function() {
                location.href = "/home"
            })
        }
    });
}

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
                // alert("The bikeID cannot be empty");
                callModalAlert("ERROR", "The bikeID cannot be empty")
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
                // alert("Please input correct BikeID!");
                callModalAlert("ERROR", "Please input correct BikeID!")
            }
            else if (response.state == 1) {
                // alert("This Bike cannot be used now!");
                callModalAlert("ERROR", "This Bike cannot be used now!")
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
        //alert("The bikeID cannot be empty");
        callModalAlert("ERROR", "The bikeID cannot be empty")
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
        //alert("Success! - This report has been sent to us.");
        callModalAlert("SUCCESS", "This report has been sent to us")
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
                //alert("The bikeID cannot be empty");
                callModalAlert("ERROR", "The bikeID cannot be empty")
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
