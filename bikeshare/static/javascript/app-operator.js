// Init basic global variables
let map;
let markersList = []
let markerBallonList = []
let markerBikeList = []
let markerBikeListMoving = []
let markerBikeListMovingNames = []
let moveInterval;
let markerCluster;

/**
 * Populates the map with the markers and start some basic functionalities
 */
function showInitMap(results) {
    // Hide the area to select bikes
    $('#ride-bike').hide();

    // Make the REST request using a GET protocol to get all the available location with bikes
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/locations-of-availabe-bikes/",
        data: {},
        success: function (response) {
            // Save the response location as an array
            var arrayData = response.location;

            // Clean the markers on the map
            for (let j = 0; j < markerBallonList.length; j++) {
                markerBallonList[j].setMap(null);
            }
            markerBallonList = []

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

                // Add marker to the list
                markerBallonList.push(marker)
            }
        },
    });
}

/**
 * Get ongoing activities of the current operator
*/
function getPendingOps() {
    // Hide html element for pending repairs and movements
    $("#pending-movs").hide()
    $("#pending-repairs").hide()

    // Make the REST request using GET protocol to get all the pending actions
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/get-pendings-op/",
        data: {},
        success: function (response) {
            // get the arrays for pending movements and repairs
            var movs = response.movs
            var reps = response.repairs

            // If there are movements pending show the element on DOM
            if (movs.length > 0) {
                $("#pending-movs").show()
            }

            // If there are repairs pending show the element on DOM
            if (reps.length > 0) {
                $("#pending-repairs").show()
            }

            // ************** START MOVMENTS PART **************
            // String to create the html after
            let stringHtml = "";

            // Iterate over the pending movements to create the html to be displayed
            for (var x = 0; x < movs.length; x++) {

                // Get the data that it will be used after
                let cMov = movs[x];
                let possibleLoc = cMov.location
                let currentBike = cMov.bike_id

                // Validate a grid 3x3 and open or close the grid
                if (x % 3 == 0) {
                    if (x > 0) {
                        stringHtml += '</div>';
                        stringHtml += '<div class="row">';
                    }
                    else if (x == 0) {
                        stringHtml += '<div class="row">';
                    }
                }

                // Create html in a string to form the grid
                stringHtml += '<div class="col">';
                stringHtml += '	<div class="row">';
                stringHtml += '	  <div class="col grid-img-style">';
                stringHtml += '		<img class="grid-style " src="' + imgs + '/bike.png" alt="bike">';
                stringHtml += '		<h4 >Bike ' + "No. " + currentBike.bike_id + '</h4>';
                stringHtml += '	  </div>';
                stringHtml += '	</div>';
                stringHtml += '	<div class="row">';
                stringHtml += '	  <div class="col" id="accord-pendig-' + currentBike.bike_id + '">';
                stringHtml += '	  <div class="row">';

                stringHtml += '<div class="col">';
                stringHtml += '    <button ';
                stringHtml += '        class="btn btn-primary grid-style"  ';
                stringHtml += '        data-toggle="collapse" data-target="#MoveCollapsePending' + currentBike.bike_id + '" ';
                stringHtml += '        data-parent="#accord-pendig-' + currentBike.bike_id + '" aria-controls="MoveCollapsePending' + currentBike.bike_id + '" ';
                //stringHtml+='        onClick="GetMove('+currentBike.bike_id+')"> ';
                stringHtml += '        > ';
                stringHtml += '            Move ';
                stringHtml += '    </button> ';
                stringHtml += '	  </div>';
                stringHtml += '	  </div>';
                stringHtml += '	  <div class="row">';
                stringHtml += '<div class="col">';

                stringHtml += ' ';
                stringHtml += '    <div class="collapse" id="MoveCollapsePending' + currentBike.bike_id + '" data-parent="#accord-pendig-' + currentBike.bike_id + '"> ';
                stringHtml += '        <div class="card card-body"> ';
                stringHtml += '            <div id="MoveCollapsePending' + currentBike.bike_id + 'Body"> ';
                stringHtml += '                  The proposed new location is loaded below, if you want to drop the bike in another location just change the postcode below  ';
                stringHtml += '            </div> ';
                stringHtml += '        </div> ';
                stringHtml += '        <div class="card-footer" > ';
                stringHtml += '            <div class="form-group"> ';
                stringHtml += '                <label for="postcode">Enter the new postcode, you would like to move the bike to: </label> ';
                stringHtml += '                <input class="form-control" ';
                stringHtml += '                    placeholder="Enter new postcode" ';
                stringHtml += '                    type="text" ';
                stringHtml += '                    value="' + possibleLoc.postcode + '" ';
                stringHtml += '                    id="NewPostcodeMove' + currentBike.bike_id + '" ';
                stringHtml += '                    class="box" ';
                stringHtml += '                /> ';
                stringHtml += '            </div> ';
                stringHtml += '            <div class="form-group"> ';
                stringHtml += '                <button  ';
                stringHtml += '                    type="button" class="btn btn-success" id="ConfirmMove"  ';
                stringHtml += '                    onclick="MoveLocationFinish(' + currentBike.bike_id + ')"> ';
                stringHtml += '                    Finish Moving ';
                stringHtml += '                </button>   ';
                stringHtml += '            </div> ';
                stringHtml += '        </div> ';
                stringHtml += '    </div> ';
                stringHtml += '	  </div>';
                stringHtml += '	  </div>';
                stringHtml += '	  </div>';
                stringHtml += '	</div>';
                stringHtml += '</div>';
            }

            // Close the grid and validate if the row is full or not
            var neededOnGrid = 3 - (movs.length % 3);
            if ((movs.length % 3) == 0) {
                neededOnGrid = 0
            }
            for (let x = 0; x < neededOnGrid; x++) {
                stringHtml += '<div class="col"></div>';
            }
            stringHtml += '</div>'

            // Add the string html to the DOM
            $("#main-pending-movs").html(stringHtml)

            // ************** START REPAIRS PART **************

            // Restart the stringHtml variable to be used for the repairs
            stringHtml = "";

            // Iterate over all the repairs to create the html
            for (var x = 0; x < reps.length; x++) {

                // Get the data that it will be used
                let cRep = reps[x];
                let currentBike = cRep

                // Validate a grid 3x3 and close or open a row
                if (x % 3 == 0) {
                    if (x > 0) {
                        stringHtml += '</div>';
                        stringHtml += '<div class="row">';
                    }
                    else if (x == 0) {
                        stringHtml += '<div class="row">';
                    }
                }

                // Create the html inside a string 
                stringHtml += '<div class="col">';
                stringHtml += '	<div class="row">';
                stringHtml += '	  <div class="col grid-img-style">';
                stringHtml += '		<img class="grid-style " src="' + imgs + '/bike.png" alt="bike">';
                stringHtml += '		<h4 >Bike ' + "No. " + currentBike.bike_id + '</h4>';
                stringHtml += '	  </div>';
                stringHtml += '	</div>';
                stringHtml += '	<div class="row">';
                stringHtml += '	  <div class="col" id="accord-pendig-' + currentBike.bike_id + '">';
                stringHtml += '	  <div class="row">';
                stringHtml += '<div class="col">';
                stringHtml += '    <button ';
                stringHtml += '        class="btn btn-primary grid-style"  ';
                stringHtml += '        data-toggle="collapse" data-target="#RepairCollapsePending' + currentBike.bike_id + '" ';
                stringHtml += '        data-parent="#accord-pendig-' + currentBike.bike_id + '" aria-controls="RepairCollapsePending' + currentBike.bike_id + '" ';
                //stringHtml+='        onClick="GetRepair('+currentBike.bike_id+')"> ';
                stringHtml += '        > ';
                stringHtml += '            Repair ';
                stringHtml += '    </button> ';
                stringHtml += '	  </div>';

                stringHtml += '	  </div>';
                stringHtml += '	  <div class="row">';
                stringHtml += '<div class="col">';
                stringHtml += '    <div class="collapse" id="RepairCollapsePending' + currentBike.bike_id + '" data-parent="#accord-pendig-' + currentBike.bike_id + '"> ';
                stringHtml += '        <div class="card card-body" ';
                stringHtml += '            id="RepairCollapsePending' + currentBike.bike_id + 'Body"> ';
                stringHtml += '                    You are working on the repairments of this bike';
                stringHtml += '        </div> ';
                stringHtml += '        <div class="card-footer"> ';
                /*stringHtml+='            <div class="form-group"> ';
                stringHtml+='                <label for="postcode">Here are some comments from customers: </label> ';
                stringHtml+='            </div> ';*/
                stringHtml += '            <div class="form-group"> ';
                stringHtml += '                <button ';
                stringHtml += '                    class="submitbox btn btn-success" ';
                stringHtml += '                    onclick="BikeRepairedFinish(' + currentBike.bike_id + ')" ';
                stringHtml += '                    > ';
                stringHtml += '                    Finish Repair Bike ';
                stringHtml += '                </button> ';
                stringHtml += '            </div> ';
                stringHtml += '        </div> ';
                stringHtml += '    </div>   ';
                stringHtml += ' ';

                stringHtml += '	  </div>';
                stringHtml += '	  </div>';
                stringHtml += '	  </div>';
                stringHtml += '	</div>';
                stringHtml += '</div>';
            }

            // Close the grid depending of how full is the row
            var neededOnGrid = 3 - (reps.length % 3);
            if ((reps.length % 3) == 0) {
                neededOnGrid = 0
            }
            for (let x = 0; x < neededOnGrid; x++) {
                stringHtml += '<div class="col"></div>';
            }
            stringHtml += '</div>'

            // Add the html string to the DOM
            $("#main-pending-repairs").html(stringHtml)
        },
    });
}

/**
 * Update the map when the customer selects a location to look for bikes
 * 
 * @param {JQuery|HTMLElement} postcode -  The postcode value on the input
*/
function getBikesOperator(results) {
    // Get the postcode valude
    var postcode = $("#postcode").val()
    // Validate the postcode is not empty neither only spaces
    if (postcode.split(' ').join('').length == 0) {
        // In case the input is empty
        alert("ERROR: Please write a postcode")
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
                        icon: image,
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

                    // Text to display on the interface/view
                    let defectiveText = ""
                    let defectiveStyle = ""
                    let defectiveHide = ""
                    let moveHide = ""
                    let moveText = "Moving bike..."
                    // Check if the bike has no report 
                    if (currentBike.is_defective == 0) {
                        defectiveText = "This bike has no report. But you can do a repair maintenance"
                    }
                    else {
                        // If bike has report add comments from the reports
                        defectiveText = "Here are some comments from customers:"
                        // Text for style
                        defectiveStyle = "style='color:red; font-weight:bold'"
                        // If has reportst
                        if (currentBike.reports.length > 0) {
                            // Get the first report
                            let report0 = currentBike.reports[0]
                            // Check if the report has no operator assigned
                            if (report0.assigned_operator == null) {
                                defectiveText = "This bike is defective but has not been assigned. You can repair it"
                                defectiveText += " <br>Here are some comments from customers:"
                                // Add the comments from customers
                                for (let df = 0; df < currentBike.reports.length; df++) {
                                    let currentRep = currentBike.reports[df]
                                    defectiveText += "<br> -" + currentRep.issue
                                }
                            }
                            // If the assigned operator has the same ID as the one making the query
                            else if (report0.assigned_operator.user_id != $.cookie("userid")) {
                                // Set text for message and style
                                defectiveText = "This bike is defective but has been assigned to other operator"
                                defectiveStyle = "style='color:#c5c546; font-weight:bold'"
                                // If the bike is being repared by another operator
                                if (report0.in_progress == 1) {
                                    defectiveText = "This bike is being reparted by another operator"
                                    moveHide = "style='display:none'"
                                    moveText = "You cannot move this bike because is being worked by an operator"
                                }
                                // Style for defective bikes
                                defectiveHide = "style='display:none'"
                            }
                            else {
                                // If bike has operator as assigned one
                                defectiveText = "This was has been assigned to you."
                                defectiveText += " <br>Here are some comments from customers:"
                                for (let df = 0; df < currentBike.reports.length; df++) {
                                    // Add comments
                                    let currentRep = currentBike.reports[df]
                                    defectiveText += "<br> -" + currentRep.issue
                                }
                            }
                        }
                    }

                    // Add a column per bike on the DOM
                    stringHtml += '<div class="col">';
                    stringHtml += '	<div class="row">';
                    stringHtml += '	  <div class="col grid-img-style">';
                    stringHtml += '		<img class="grid-style " src="' + imgs + '/bike.png" alt="bike">';
                    stringHtml += '		<h4 ' + defectiveStyle + '>Bike ' + "No. " + currentBike.bike_id + '</h4>';
                    stringHtml += '	  </div>';
                    stringHtml += '	</div>';
                    stringHtml += '	<div class="row">';
                    stringHtml += '	  <div class="col" id="accord-' + currentBike.bike_id + '">';
                    stringHtml += '	  <div class="row">';
                    stringHtml += '<div class="col">';
                    stringHtml += '    <button ';
                    stringHtml += '        class="btn btn-primary grid-style"  ';
                    stringHtml += '        data-toggle="collapse" data-target="#RepairCollapse' + currentBike.bike_id + '" ';
                    stringHtml += '        data-parent="#accord-' + currentBike.bike_id + '" aria-controls="RepairCollapse' + currentBike.bike_id + '" ';
                    //stringHtml+='        onClick="GetRepair('+currentBike.bike_id+')"> ';
                    stringHtml += '        > ';
                    stringHtml += '            Repair ';
                    stringHtml += '    </button> ';
                    stringHtml += '	  </div>';
                    stringHtml += '<div class="col">';
                    stringHtml += '    <button ';
                    stringHtml += '        class="btn btn-primary grid-style"  ';
                    stringHtml += '        data-toggle="collapse" data-target="#MoveCollapse' + currentBike.bike_id + '" ';
                    stringHtml += '        data-parent="#accord-' + currentBike.bike_id + '" aria-controls="MoveCollapse' + currentBike.bike_id + '" ';
                    //stringHtml+='        onClick="GetMove('+currentBike.bike_id+')"> ';
                    stringHtml += '       > ';
                    stringHtml += '            Move ';
                    stringHtml += '    </button> ';
                    stringHtml += '	  </div>';
                    stringHtml += '	  </div>';
                    stringHtml += '	  <div class="row">';
                    stringHtml += '<div class="col">';
                    stringHtml += '    <div class="collapse" id="RepairCollapse' + currentBike.bike_id + '" data-parent="#accord-' + currentBike.bike_id + '"> ';
                    stringHtml += '        <div class="card card-body" ';
                    stringHtml += '            id="RepairCollapse' + currentBike.bike_id + 'Body"> ';
                    stringHtml += '                    ' + defectiveText + '';
                    stringHtml += '        </div> ';
                    stringHtml += '        <div class="card-footer" ' + defectiveHide + '> ';
                    /*stringHtml+='            <div class="form-group"> ';
                    stringHtml+='                <label for="postcode">Here are some comments from customers: </label> ';
                    stringHtml+='            </div> ';*/
                    stringHtml += '            <div class="form-group"> ';
                    stringHtml += '                <button ';
                    stringHtml += '                    class="submitbox btn btn-success" ';
                    stringHtml += '                    onclick="BikeRepaired(' + currentBike.bike_id + ')" ';
                    stringHtml += '                    > ';
                    stringHtml += '                    Repair Bike ';
                    stringHtml += '                </button> ';
                    stringHtml += '            </div> ';
                    stringHtml += '        </div> ';
                    stringHtml += '    </div>   ';
                    stringHtml += ' ';
                    stringHtml += '    <div class="collapse" id="MoveCollapse' + currentBike.bike_id + '" data-parent="#accord-' + currentBike.bike_id + '"> ';
                    stringHtml += '        <div class="card card-body"> ';
                    stringHtml += '            <div id="MoveCollapse' + currentBike.bike_id + 'Body"> ';
                    stringHtml += '                    ' + moveText + '';
                    stringHtml += '            </div> ';
                    stringHtml += '        </div> ';
                    stringHtml += '        <div class="card-footer" ' + moveHide + '> ';
                    stringHtml += '            <div class="form-group"> ';
                    stringHtml += '                <label for="postcode">Enter the new postcode, you would like to move the bike to: </label> ';
                    stringHtml += '                <input class="form-control" ';
                    stringHtml += '                    placeholder="Enter new postcode" ';
                    stringHtml += '                    type="text" ';
                    stringHtml += '                    id="NewPostcode' + currentBike.bike_id + '" ';
                    stringHtml += '                    class="box" ';
                    stringHtml += '                /> ';
                    stringHtml += '            </div> ';
                    stringHtml += '            <div class="form-group"> ';
                    /*stringHtml+='                <button ';
                    stringHtml+='                    class="submitbox btn btn-primary" ';
                    stringHtml+='                    onclick="getBikes()" ';
                    stringHtml+='                > Search ';
                    stringHtml+='                </button>               ';*/
                    stringHtml += '                <button  ';
                    stringHtml += '                    type="button" class="btn btn-success" id="ConfirmMove"  ';
                    stringHtml += '                    onclick="MoveLocation(' + currentBike.bike_id + ')"> ';
                    stringHtml += '                    Move to Location ';
                    stringHtml += '                </button>   ';
                    stringHtml += '            </div> ';
                    stringHtml += '        </div> ';
                    stringHtml += '    </div> ';
                    stringHtml += '	  </div>';
                    stringHtml += '	  </div>';
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
        });
    }
}

/**
 * Track bikes on the interface
*/
function GetTrack() {
    //var html="Current Bike ID: "+$("#bikeid").val()+"<br>"+"Current Location: "+$("#postcode").val();

    // Make REST request using GET protocol to get all the bikes and their status
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/track-bikes/",
        data: {},
        success: function (response) {
            // Save response data
            var data = response.data;
            // Clean interval if exists - This is for the animations
            clearInterval(moveInterval);

            // Clean the markers positions
            for (let j = 0; j < markersList.length; j++) {
                markersList[j].setMap(null);
            }
            markersList = []

            // Clean the marker locations
            for (let k = 0; k < markerBallonList.length; k++) {
                markerBallonList[k].setMap(null);
            }
            markerBallonList = []

            // Clean the makers bikes
            for (let l = 0; l < markerBikeList.length; l++) {
                markerBikeList[l].setMap(null);
            }
            markerBikeList = []

            // Clean the clusters
            if (markerCluster) {
                markerCluster.clearMarkers();
            }

            // Get the bikes that are currently moving and remove them from the map
            for (let p = 0; p < markerBikeListMoving.length; p++) {
                markerBikeListMoving[p].setMap(null);
            }
            markerBikeListMoving = []
            markerBikeListMovingNames = []

            // Set new center of the map
            var center = new google.maps.LatLng(55.860789, -4.250311);

            // Animation of transcition in the map
            window.setTimeout(() => {
                map.panTo(center);
                map.setZoom(12);
                map.setCenter(center);
            }, 30);

            // Image marker using a bike icon
            const image = {
                url: imgs + '/bike.png',
                origin: new google.maps.Point(0, 0),
                scaledSize: new google.maps.Size(60, 60),
            };

            // These are constant to show bike icon on maps
            var pi = Math.PI
            var degrees = 180;
            var radious = 0.001; //0.0001 - 
            var randomess_l1 = 100
            var randomess_l2 = 200
            var listBikesOps = []

            // Iterate over the bikes returned by API
            for (let m = 0; m < data.length; m++) {
                // Get current data
                let currentB = data[m]
                let bikeLocation = currentB.location

                // Get the latitude of the bike's location
                var longitudeData = bikeLocation.longitude;
                var latitudeData = bikeLocation.latitude;

                // The way to display the bike markers on the map was based on the following
                // Mahdi. How to place markers on the outline of a circle in google maps?. 
                // On: https://gis.stackexchange.com/questions/37615/how-to-place-markers-on-the-outline-of-a-circle-in-google-maps
                // Accesed on: Feb, 11 2021
                var randomness_degrees = Math.floor(Math.random() * (randomess_l2 - randomess_l1) + randomess_l1);
                var longitudeBike = Math.cos(randomness_degrees * pi / 180) * radious + longitudeData;
                var latitudeBike = Math.sin(randomness_degrees * pi / 180) * radious + latitudeData;

                // Create a latitude and longitude object to place the bike
                var myLatLong = new google.maps.LatLng(latitudeBike, longitudeBike);

                // Set the new bike marker
                const marker = new google.maps.Marker({
                    position: myLatLong,
                    title: "bike_: " + (currentB.bike_id),
                    icon: image,
                    label: {
                        text: "No. " + currentB.bike_id,
                        color: "#ffffff",
                        fontSize: "20px",
                        fontWeight: "bold"
                    },
                })


                // First get the current rented bikes
                if (currentB.is_available == 0 && currentB.is_defective == 0) {
                    const markerMov = new google.maps.Marker({
                        position: myLatLong,
                        map: map,
                        title: "bike_: " + (currentB.bike_id),
                        icon: image,
                        label: {
                            text: "No. " + currentB.bike_id,
                            color: "#ffffff",
                            fontSize: "20px",
                            fontWeight: "bold"
                        },
                    })
                    // Add marker to the corresponding lists
                    markerBikeListMoving.push(markerMov)
                    markerBikeListMovingNames.push(currentB)
                }
                // Second get the available bikes to be clustered
                else if (currentB.is_available == 1) {
                    markerBikeList.push(marker)
                }
                // Finally get the list of bike with some extra property (repairing or moving)
                else {
                    listBikesOps.push(currentB)
                }
            }

            // Create cluster of markers
            markerCluster = new MarkerClusterer(map, markerBikeList, {
                maxZoom: 15,
                imagePath:
                    "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
            });

            // generate text to tell status of bikes under operations (repairs and movements)
            let innerTextOps = ""
            for (var u = 0; u < listBikesOps.length; u++) {
                // Get the data
                var cBk = listBikesOps[u]

                // If bike is moving
                if (cBk.is_available == 2) { // move
                    innerTextOps += "<p><b>Bike No. " + cBk.bike_id + ":</b> It's being moved</p>"
                }
                // If bike is being repaired
                else if (cBk.is_available == 3) { // repairing
                    innerTextOps += "<p><b>Bike No. " + cBk.bike_id + ":</b> It's under repairment</p>"
                }
                // error case 
                else {
                    innerTextOps += "<p><b>Bike No. " + cBk.bike_id + ":</b> No idea. Contact admin</p>"
                }
            }
            // If there is no bike under any extra activity
            if (listBikesOps.length == 0) {
                innerTextOps = "<b> There is no bike under any activity by operators</b>"
            }

            // List the bikes that are currently rented
            innerTextOps += "<b>Bikes currently rented: </b>"
            for (var m = 0; m < markerBikeListMovingNames.length; m++) {
                var cUBk = markerBikeListMovingNames[m]
                innerTextOps += "<p>Bike No. " + cUBk.bike_id + "</p>"
            }

            // Add string html to DOM
            $("#TrackCollapseBody").html(innerTextOps);

            // Add animation of bikes rented on the map
            // This is simulated with the routes in the script routes.js
            let counterInterval = 0
            moveInterval = setInterval(function () {
                for (var u = 0; u < markerBikeListMoving.length; u++) {
                    var currRoute = routes_map['route' + ((u % 5) + 1)]
                    if (counterInterval < currRoute.length) {
                        var currCorr = currRoute[counterInterval]
                        markerBikeListMoving[u].setPosition(new google.maps.LatLng(currCorr.lat, currCorr.lng));
                    }
                }
                counterInterval++
            }, 500);
        }
    });
}

/**
 * Resets the interface when ending tracking bikes
 * 
*/
function EndTrack() {
    // Clear interval of animations
    clearInterval(moveInterval);

    // Clean list of markers
    for (let j = 0; j < markersList.length; j++) {
        markersList[j].setMap(null);
    }
    markersList = []

    // Clean list of locations
    for (let k = 0; k < markerBallonList.length; k++) {
        markerBallonList[k].setMap(null);
    }
    markerBallonList = []

    // Clean list of bikes markers
    for (let l = 0; l < markerBikeList.length; l++) {
        markerBikeList[l].setMap(null);
    }
    markerBikeList = []

    // Clear cluster markers
    if (markerCluster) {
        markerCluster.clearMarkers();
    }

    // Clear bikes moving markers
    for (let p = 0; p < markerBikeListMoving.length; p++) {
        markerBikeListMoving[p].setMap(null);
    }
    markerBikeListMoving = []
    markerBikeListMovingNames = []

    // Call functions to restart interface
    showInitMap();
    getPendingOps();
}

/**
 * Starts the bike repair calling the API endpoint that corresponds
 * 
 * @param {int} bikeId -  The bike id that is starting the repair
 * @param {JQuery|Cookie} xcsrft -  The cookie
*/
function BikeRepaired(bikeId) {

    // HTML code intented to be used as a message
    var html = "Current Bike ID: " + $("#bikeid").val() + "<br>"
        + "Current Location: " + $("#postcode").val() + "<br>"
        + "Current Repair Status: " + "None";
    $("#RepairCollapseBody").html(html);

    // The token
    var xcsrft = $.cookie("csrftoken")

    // Make a REST request using POST protocol to start repair
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/bike-repaired-by-operator-start/",
        data: {
            bike_id: bikeId
        },
        beforeSend: function (request) {
            // Set the CSRF token before send since Django expected that way
            request.setRequestHeader("X-CSRFToken", xcsrft);
        },
        success: function (response) {
            // Alert of the new state of the bike
            var data = response.data;
            alert("The repairment has started.");
            // Refresh the current view
            getBikesOperator();
            getPendingOps();
        }
    });
}

/**
 * Finishes the bike repair calling the API endpoint that corresponds
 * 
 * @param {int} bikeId -  The bike id that is finishing the repair
 * @param {JQuery|Cookie} xcsrft -  The cookie
*/
function BikeRepairedFinish(bikeId) {
    // The token
    var xcsrft = $.cookie("csrftoken")

    // Make a REST request using POST protocol to finish repair
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/bike-repaired-by-operator-end/",
        data: {
            bike_id: bikeId
        },
        beforeSend: function (request) {
            // Set the CSRF token before send since Django expected that way
            request.setRequestHeader("X-CSRFToken", xcsrft);
        },
        success: function (response) {
            // Alert of the new state of the bike
            var data = response.data;
            alert("The repairment has ended. The bike will be returned to the last location where it was");
            // Refresh the current view
            getPendingOps();
            getBikesOperator();
        }
    });
}

/**
 * Starts the bike movement calling the API endpoint that corresponds
 * 
 * @param {int} bikeId -  The bike id that is starting to be moved
 * @param {JQuery|Cookie} xcsrft -  The cookie
 * @param {JQuery|HTMLElement} NewPostcode - The new intended position of the bike
*/
function MoveLocation(bikeId) {

    // The token
    var xcsrft = $.cookie("csrftoken")

    // Get the value of the new postcode
    var NewPostcode = document.querySelector("#NewPostcode" + bikeId).value;
    // Check if empty
    if (NewPostcode == "" || NewPostcode == "") {
        alert("Please enter the new postcode.");
    } else {
        // Make a REST request using POST protocol to start the movement of the bike
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/bike-move-start/",
            data: {
                bike_id: bikeId,
                place: $("#NewPostcode" + bikeId).val()
            },
            beforeSend: function (request) {
                // Set the CSRF token before send since Django expected that way
                request.setRequestHeader("X-CSRFToken", xcsrft);
            },
            success: function (response) {
                // Alert of the new state of the bike
                var data = response.data;
                alert("Bike movement has started.");
                // Refresh the current view
                getBikesOperator();
                getPendingOps();
            }
        });
    };
};

/**
 * Finishes the bike movement calling the API endpoint that corresponds
 * @param {int} bikeId -  The bike id that is finishing to be moved
 * @param {JQuery|Cookie} xcsrft -  The cookie
 * @param {JQuery|HTMLElement} NewPostcode - The new intended position of the bike
*/
function MoveLocationFinish(bikeId) {
    // The token
    var xcsrft = $.cookie("csrftoken")
    // Getting the value of the postcode
    var NewPostcode = $("#NewPostcodeMove" + bikeId).val();

    // Check if empty
    if (NewPostcode == "" || NewPostcode == "") {
        alert("Please enter the new postcode.");
    } else {
        // Make a REST request using POST protocol to end the movement of the bike
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/bike-move-end/",
            data: {
                bike_id: bikeId,
                place: NewPostcode
            },
            beforeSend: function (request) {
                // Set the CSRF token before send since Django expected that way
                request.setRequestHeader("X-CSRFToken", xcsrft);
            },
            success: function (response) {
                // Alert of the new state of the bike
                var data = response.data;
                alert("Bike movement has finished.");
                // Refresh the current view
                getBikesOperator();
                getPendingOps();
            }
        });
    };
}