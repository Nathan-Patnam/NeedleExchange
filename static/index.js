
// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.

// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

function initAutocomplete() {
    var latlng = new google.maps.LatLng(37.09024, -95.712891);
    var myOptions = {
        zoom: 5,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    var map = new google.maps.Map(document.getElementById("map"), myOptions);



    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);


    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

    })
}

function sendAddress(){
    var userAddress =  $("#pac-input").val();
    var sendInfo={
        address:userAddress
    };

    $.ajax({
        url: "http://10.194.29.0:9000/find",
        type: "POST",
        dataType: "json",
        success: function (msg) {
            if (msg) {
                alert("Somebody" + name + " was added in list !");
                location.reload(true);
            } else {
                alert("Cannot add to list !");
            }
        },


        data: sendInfo
    });

}
