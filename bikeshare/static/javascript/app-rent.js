/**
 * This file contains the rent logic to be executed user_page.html
 */

/**
 * Calls the API when returning a bike is needed
 * @param {Django|Element} trip_id -  The id of the trip to be ended
 * @param {JQuery|HTMLElement} currentLocation -  The location where the bike is gonna be left
 * @param {JQuery|Cookie} xcsrft -  The cookie
 */
function returnBike() {
    // Get the variables of postcode and the token
    var currentLocation = $("#postcode-return").val()
    // Remove spaces
    currentLocation = currentLocation.replace(' ', '')
    var xcsrft = $.cookie("csrftoken")
    // Call an alert if the location is empty
    if (currentLocation.length == 0) {
        //alert("Write the postcode please");
        callModalAlert("ERROR", "Write the postcode please")
    }
    else {
        // Quit timer
        clearInterval(timer);

        // Make the REST request using POST request to return the bike
        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/return_bike/",
            data: {
                // Add the data on the request which includes the bike id, the address and the trip
                bike_id: bike,
                location: currentLocation,
                trip_id: trip_id
            },
            beforeSend: function (request) {
                // Set the CSRF token before send since Django expected that way
                request.setRequestHeader("X-CSRFToken", xcsrft);
            },
            success: function (response) {
                // If the API responses is correct
                var data = response.data;
                // Get the total to be payed
                var costDisplay = Math.round(data.cost * 100) / 100
                // Show payment modal
                $('#payment').modal('show');
                // Add the text of the payment
                $("#payment-info-modal").text("Your total cost is: " + costDisplay)
                // Add the currentCost as a window variable
                window.currentCost = data.cost;
            },
            error: function (response, textStatus, errorThrown) {
                // If location is not found
                if (response.status == 404) {
                    //alert("This is not a valid postcode/address. Please enter a correct one")
                    callModalAlert("ERROR", "This is not a valid postcode/address. Please enter a correct one")
                }
            }
        });
    }
}

/**
 * Call when users make the payment if fonds are enough. 
 * @param {Window|Element} currentCost -  The cost to be payed
 * @param {JQuery|Cookie} xcsrft -  The cookie
 */
function makePayment() {
    // should check the user profile before make the payment
    var currentCost = -1 * window.currentCost
    var xcsrft = $.cookie("csrftoken")

    // Make a REST request using a POST protocol to make the payment from the wallet
    $.ajax({
        type: "POST",
        dataType: "json",
        url: "/recalculate-wallet/",
        data: {
            // Add the amount to be payed to the request
            amount: currentCost
        },
        beforeSend: function (request) {
            // Set the CSRF token before send since Django expected that way
            request.setRequestHeader("X-CSRFToken", xcsrft);
        },
        success: function (response) {
            // If the API responds correctly show to the user if it has a debt or how much is the available money in its wallet
            var data = response.data;
            var credit = data.credit
            var text = ""
            if (credit < 0) {
                // If there is a debt
                //alert("You have a debt of " + (-1 * credit) + ". You will need to add enough money to your wallet before riding again")
                text = "You have a debt of " + (-1 * credit) + ". You will need to add enough money to your wallet before riding again"
            }
            else {
                // If there is not debt show the credit on wallet
                text = "You have payed your ride. Your current credit is " + credit
            }
            // Go to home page
            callModalAlert("INFO", text, function() {
                location.href = "/home"
            })
        }
    });
}


/**
 * Format number to be showed on the count down
 * @param {intenger} num - The number to be formated
 * @returns {string} numstr - The formated number
 */
function showNum(num) {
    // If the num is less than 10 then add a 0 before 
    if (num < 10) {
        return "0" + num;
    } else {
        // if the number is greater than 10 then just return the number
        return num;
    }
}