/**
 * This file contains the manager logic to be executed user_page.html
 */

// Global variables to be used
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
    // Set date max on end date picker with default values - it should be current date
    var maxDate = new Date()
    var maxDateIso = maxDate.toISOString()
    var maxDateValue = maxDateIso.split("T")[0]
    // Set value on DOM element
    $("#end-date-report").val(maxDateValue)

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
 * Track bikes on the interface
*/
function GetTrack() {

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
                    //console.log(randomness_degrees)
                    ///console.log(bikeLocation.postcode)
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
}

/**
 * Download in a csv the trips on a date range
 * 
 * @param {JQuery|HTMLElement} d1 - Start date
 * @param {JQuery|HTMLElement} d2 - End date
*/
function DownloadHistoryTrips() {

    // Crate date object from the date given from the inputs
    var d1 = $("#start-date-report").val()
    var d1Array = d1.split('-')
    var dateStart = new Date(d1Array[0], d1Array[1] - 1, d1Array[2])
    var d2 = $("#end-date-report").val()
    var d2Array = d2.split('-')
    var dateEnd = new Date(d2Array[0], d2Array[1] - 1, d2Array[2])

    // Convert date to a string format to be used for the API
    var dateStartStr = dateStart.toLocaleDateString("en-US", { month: '2-digit', day: '2-digit', year: 'numeric' })
    var dateStarEnd = dateEnd.toLocaleDateString("en-US", { month: '2-digit', day: '2-digit', year: 'numeric' })

    // Make the REST request using GET protocol to get all the trips in the data range
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/trips_in_daterange",
        data: {
            start_date: dateStartStr,
            end_date: dateStarEnd
        },
        success: function (response) {

            // Get the data from the response
            var data = response.data;

            // Format the data in a way a csv could be created
            var infoCsv = "Bike, Cost, Date, Start Address, End Address, User\n"
            for (var i = 0; i < data.length; i++) {
                var currentRow = data[i]
                var currentDate = new Date(currentRow['date']).toLocaleDateString("en-US", { month: '2-digit', day: '2-digit', year: 'numeric' })
                infoCsv += currentRow.bike.bike_id + ", "
                infoCsv += currentRow.cost + ", "
                infoCsv += currentDate + ", "
                infoCsv += currentRow.start_address.line_1 + " - " + currentRow.start_address.postcode + ", "
                infoCsv += currentRow.end_address.line_1 + " - " + currentRow.end_address.postcode + ", "
                infoCsv += currentRow.user.user_id + "\n "
            }

            // To download the string formated before in a CSV way
            /**
             * Based on: John, Xavier. (2014). How to export JavaScript array info to csv (on client side)?. 
             * https://stackoverflow.com/questions/14964035/how-to-export-javascript-array-info-to-csv-on-client-side
             * Accessed on: 22/02/2021
            */
            // Create a blob object
            var blobReport = new Blob([infoCsv], { type: 'text/csv;charset=utf-8;' })
            // Create a dummy anchor element
            var linkReport = document.createElement("a")
            // Create a link object with the blob object
            var urlReport = URL.createObjectURL(blobReport)
            // Set the url on the anchor element
            linkReport.setAttribute("href", urlReport)
            // Set the name of the file that will be downloaded
            linkReport.setAttribute("download", "report-trips-" + dateStartStr + "-" + dateStarEnd + ".csv")
            // Set the anchor as not visible
            linkReport.style.visibility = 'hidden'
            // At the anchor element to DOM
            document.body.appendChild(linkReport)
            // Simulate the click on the DOM
            linkReport.click()
            // Remove the anchor element created
            document.body.removeChild(linkReport)
        }
    });
}

/**
 * Print the page on button click
 * It hides some part of the html page based on css classes
 * 
*/
function DownloadPDF() {
    print()
}

/**
 * Create the graph and table grid on the view with the report information
 * 
 * @param {JQuery|HTMLElement} d1 - Start date
 * @param {JQuery|HTMLElement} d2 - End date
*/
function generateReport() {

    // Crate date object from the date given from the inputs
    var d1 = $("#start-date-report").val()
    var d1Array = d1.split('-')
    var dateStart = new Date(d1Array[0], d1Array[1] - 1, d1Array[2])
    var d2 = $("#end-date-report").val()
    var d2Array = d2.split('-')
    var dateEnd = new Date(d2Array[0], d2Array[1] - 1, d2Array[2])

    // Convert date to a string format to be used for the API
    var dateStartStr = dateStart.toLocaleDateString("en-US", { month: '2-digit', day: '2-digit', year: 'numeric' })
    var dateStarEnd = dateEnd.toLocaleDateString("en-US", { month: '2-digit', day: '2-digit', year: 'numeric' })

    // Make the REST request using GET protocol to get the Total income
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/total_income",
        data: {
            // Set the dates on the request
            start_date: dateStartStr,
            end_date: dateStarEnd
        },
        success: function (response) {

            // Get the data
            var data = response.data;
            var text = "No info"
            if (data.length > 0) {
                text = data[0].toFixed(2)
            }

            // Set the data on the DOM element
            $("#total-income").text(text)
        }
    });

    // Make the REST request using GET protocol to get the Trip count
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/trip_count",
        data: {
            // Set the dates on the request
            start_date: dateStartStr,
            end_date: dateStarEnd
        },
        success: function (response) {

            // Get the data
            var data = response.data;
            var text = "No info"
            if (data.length > 0) {
                text = data[0]
            }

            // Set the data on the DOM element
            $("#total-trips").text(text)
        }
    });

    // Make the REST request using GET protocol to get the Most common locations:
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/most_common_locations",
        data: {
            // Set the dates on the request
            start_date: dateStartStr,
            end_date: dateStarEnd
        },
        success: function (response) {

            // Get the data
            var data = response.data;
            var text1 = data.most_common_start.line_1 + ", " + data.most_common_start.postcode
            var text2 = data.most_common_end.line_1 + ", " + data.most_common_end.postcode

            // Set the data on the DOM element
            $("#common-start").text(text1)
            $("#common-end").text(text2)
        }
    });

    // Make the REST request using GET protocol to get the average trip duration, average pay
    $.ajax({
        type: "GET",
        dataType: "json",
        url: "/report-data",
        data: {
            // Set the dates on the request
            start_date: dateStartStr,
            end_date: dateStarEnd
        },
        success: function (response) {

            // Get the data of bikes
            var data = response.data;
            var popularBike = "No. " + response.popular_bike.bike
            var profBike = "No. " + response.profit_bike.bike

            // Set the data on the DOM element
            $("#popular-bike").text(popularBike)
            $("#profitable-bike").text(profBike)

            // Get the data of repairs and movements
            var totalRep = response.cnt_repair_bikes
            var totalMov = response.cnt_moving_bikes
            var opeReap = response.opera_most_repa.opera.split("@")[0]
            var opeMove = response.opera_most_movs.opera.split("@")[0]

            // Set the data on the DOM element
            $("#total-repaired").text(totalRep)
            $("#total-moved").text(totalMov)
            $("#ope-repairs").text(opeReap)
            $("#ope-moves").text(opeMove)

            // Get the data in a html string of moving bikes
            var mvngBikes = ""
            for (var i = 0; i < response.moving_bikes.length; i++) {
                mvngBikes += "No. " + response.moving_bikes[i].bike_id + "<br>"
            }

            // Get the data in a html string of the repairs bike
            var rprBikes = ""
            for (var j = 0; j < response.repairing_bikes.length; j++) {
                rprBikes += "No. " + response.repairing_bikes[j].bike_id + "<br>"
            }

            // Set the data on the DOM element
            $("#current-moves").html(mvngBikes)
            $("#current-repairs").html(rprBikes)

            // Array with the possible colors to be used
            var colors_array = ["#d8d4ea", "#004fa4", "#eb1629", "#05173e", '#e51837', "#0477c2", "#0082c4", "#f0c1b3", "#9bcfd0", "#bd959f", "#989887", "#f6b969", "#037272", "#acc5c8", "#dac45f", "#c2a248", "#93b8d3", "#c0cbc0", "#a5b1a8", "#8e8e96", "#66695c"]

            // Create the Timeline of the trips and income per day
            var maxDate = null;
            var minDate = null;
            // Create the date objects
            if (response.trip_count_per_day) {
                maxDate = new Date(response.trip_count_per_day[0].date_start)
                minDate = new Date(response.trip_count_per_day[0].date_start)
            }

            // Check for the min an max dates on trips
            for (var a = 0; a < response.trip_count_per_day.length; a++) {
                var r = response.trip_count_per_day[a]
                if (new Date(r.date_start) > maxDate) {
                    maxDate = new Date(r.date_start)
                }
                if (new Date(r.date_start) < minDate) {
                    minDate = new Date(r.date_start)
                }
            }

            // Check for the min an max dates on income
            var maxDatePay = null;
            var minDatePay = null;
            if (response.income_per_day) {
                maxDatePay = new Date(response.income_per_day[0].date_start)
                minDatePay = new Date(response.income_per_day[0].date_start)
            }
            for (var a = 0; a < response.income_per_day.length; a++) {
                var r = response.income_per_day[a]
                if (new Date(r.date_start) > maxDatePay) {
                    maxDatePay = new Date(r.date_start)
                }
                if (new Date(r.date_start) < minDatePay) {
                    minDatePay = new Date(r.date_start)
                }
            }

            // Calculate the real min and max from the data
            var realMax = null
            var realMin = null
            if (maxDatePay > maxDate) {
                realMax = maxDatePay
            }
            else {
                realMax = maxDate
            }
            if (minDatePay < minDate) {
                realMin = minDatePay
            }
            else {
                realMin = minDate
            }

            // Create array with dates
            var datesGraph = []
            var currentD = realMin
            while (currentD <= realMax) {
                datesGraph.push(currentD.toLocaleDateString("en-US", { month: '2-digit', day: '2-digit', year: 'numeric' }))
                currentD.setDate(currentD.getDate() + 1)
            }
            // Fill data arrays and add zero in case the date is not part of the gotten data
            var dataTrip = []
            var dataIncome = []
            for (var x = 0; x < datesGraph.length; x++) {
                var d = datesGraph[x]

                // For trips data
                var found = false
                for (var y = 0; y < response.trip_count_per_day.length; y++) {
                    var dayTrip = response.trip_count_per_day[y]
                    if (new Date(d).getTime() == new Date(dayTrip.date_start).getTime()) {
                        dataTrip.push(dayTrip.total)
                        found = true
                        break
                    }
                }
                // If not found add zero
                if (found == false) {
                    dataTrip.push(0)
                }

                // For income data
                var foundPay = false
                for (var z = 0; z < response.income_per_day.length; z++) {
                    var day = response.income_per_day[z]
                    if (new Date(d).getTime() == new Date(day.date_start).getTime()) {
                        dataIncome.push(day.total.toFixed(2))
                        foundPay = true
                        break
                    }
                }
                // If not found add zero
                if (foundPay == false) {
                    dataIncome.push(0)
                }
            }

            // Creating the timeline chart
            var timeline = {
                labels: datesGraph,
                datasets: [{
                    data: dataTrip,
                    backgroundColor: 'transparent',
                    borderColor: colors_array[0],
                    borderWidth: 4,
                    pointBackgroundColor: colors_array[0],
                    label: 'Trips',
                    yAxisID: 'Trips',
                },
                {
                    data: dataIncome,
                    backgroundColor: 'transparent',
                    borderColor: colors_array[1],
                    borderWidth: 4,
                    pointBackgroundColor: colors_array[1],
                    label: 'Income',
                    yAxisID: 'Income',
                }]
            };

            // Add the chart to the DOM
            new Chart(document.getElementById("timelines"), {
                type: 'line',
                data: timeline,
                options: {
                    scales: {
                        yAxes: [
                            {
                                id: 'Trips',
                                type: 'linear',
                                position: 'left',
                                ticks: {
                                    beginAtZero: false
                                }
                            },
                            {
                                id: 'Income',
                                type: 'linear',
                                position: 'right',
                                ticks: {
                                    beginAtZero: false
                                }
                            }
                        ]
                    },
                    legend: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: 'Trips vs Income per day'
                    }
                }
            });

            // Create the pie chart to get the average income per bike
            var labelPie = []
            var dataPie = []

            // Itereate over the data to format it into two arrays 
            for (var q = 0; q < response.average_income_per_bike.length; q++) {
                var currentBikeInc = response.average_income_per_bike[q]
                labelPie.push("No. " + currentBikeInc.bike)
                dataPie.push(currentBikeInc.total)
            }

            // Create the pie data object
            var pieData = {
                labels: labelPie,
                datasets: [
                    {
                        label: "Income Per Bike Avg",
                        backgroundColor: colors_array,
                        data: dataPie
                    }
                ]
            }

            // Add pie chart to the DOM
            new Chart(document.getElementById("income-per-bike"), {
                type: 'doughnut',
                data: pieData,
                options: {
                    title: {
                        display: true,
                        text: 'Average Income Per Bike'
                    }
                }
            });

            // Create multiple bar chart
            // Bar char to show Trip per bike
            var tripBikeLabel = []
            var tripBikeData = []

            // Itereate over the data to format it into two arrays 
            for (var t = 0; t < response.trip_per_bikes.length; t++) {
                var currentData = response.trip_per_bikes[t]
                tripBikeLabel.push("No. " + currentData.bike)
                tripBikeData.push(currentData.total)
            }

            // Create the data object to be used on the graph
            var tripBikeChartData = {
                labels: tripBikeLabel,
                datasets: [
                    {
                        label: "Trips Per Bike",
                        backgroundColor: colors_array,
                        data: tripBikeData
                    }
                ]
            }

            // Add chart to the DOM
            new Chart(document.getElementById("trip-per-bike"), {
                type: 'bar',
                data: tripBikeChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Number of Trips Per Bike'
                    },
                    legend: {
                        display: false
                    },
                }
            });

            // Bar char to show Reports per bike
            var reportsBikeLabel = []
            var reportsBikeData = []

            // Itereate over the data to format it into two arrays 
            for (var t = 0; t < response.reports_per_bike.length; t++) {
                var currentData = response.reports_per_bike[t]
                reportsBikeLabel.push("No. " + currentData.bike)
                reportsBikeData.push(currentData.bike__count)
            }

            // Create the data object to be used on the graph
            var reportBikeChartData = {
                labels: reportsBikeLabel,
                datasets: [
                    {
                        label: "Reports Per Bike",
                        backgroundColor: colors_array,
                        data: reportsBikeData
                    }
                ]
            }

            // Add chart to the DOM
            new Chart(document.getElementById("reports-per-bike"), {
                type: 'bar',
                data: reportBikeChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Number of Reports Per Bike'
                    },
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                stepSize: 1
                            }
                        }]
                    },
                }
            });

            // Bar char to show Repairs per operator 
            var reportsOpLabel = []
            var reportsOpData = []

            // Itereate over the data to format it into two arrays 
            for (var t = 0; t < response.repairs_per_operator.length; t++) {
                var currentData = response.repairs_per_operator[t]
                reportsOpLabel.push("" + currentData.opera.split("@")[0])
                reportsOpData.push(currentData.counts)
            }

            // Create the data object to be used on the graph
            var reportOpChartData = {
                labels: reportsOpLabel,
                datasets: [
                    {
                        label: "Reports Per Operator",
                        backgroundColor: colors_array,
                        data: reportsOpData
                    }
                ]
            }

            // Add chart to the DOM
            new Chart(document.getElementById("repairs-per-operator"), {
                type: 'bar',
                data: reportOpChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Number of Repairs Per Operator'
                    },
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                stepSize: 1
                            }
                        }]
                    },
                }
            });

            // Bar char to show movements per bike 
            var moveBikeLabel = []
            var moveBikeData = []

            // Itereate over the data to format it into two arrays 
            for (var t = 0; t < response.movs_per_bike.length; t++) {
                var currentData = response.movs_per_bike[t]
                moveBikeLabel.push("No. " + currentData.bike)
                moveBikeData.push(currentData.bike__count)
            }

            // Create the data object to be used on the graph
            var moveBikesChartData = {
                labels: moveBikeLabel,
                datasets: [
                    {
                        label: "Moves Per Bike",
                        backgroundColor: colors_array,
                        data: moveBikeData
                    }
                ]
            }

            // Add chart to the DOM
            new Chart(document.getElementById("movs-per-bike"), {
                type: 'bar',
                data: moveBikesChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Number of Movements Per Bike'
                    },
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                stepSize: 1
                            }
                        }]
                    },
                }
            });

            // Bar char to show movements per operator 
            var moveOpLabel = []
            var moveOpData = []

            // Itereate over the data to format it into two arrays 
            for (var t = 0; t < response.movs_per_operator.length; t++) {
                var currentData = response.movs_per_operator[t]
                moveOpLabel.push("" + currentData.opera.split("@")[0])
                moveOpData.push(currentData.counts)
            }

            // Create the data object to be used on the graph
            var moveOpsChartData = {
                labels: moveOpLabel,
                datasets: [
                    {
                        label: "Moves Per Operator",
                        backgroundColor: colors_array,
                        data: moveOpData
                    }
                ]
            }

            // Add chart to the DOM
            new Chart(document.getElementById("movs-per-operator"), {
                type: 'bar',
                data: moveOpsChartData,
                options: {
                    title: {
                        display: true,
                        text: 'Number of Movements Per Operator'
                    },
                    legend: {
                        display: false
                    },
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true,
                                stepSize: 1
                            }
                        }]
                    },
                }
            });
        }
    });
}