
// when clicking Dropdown will change
$(".dropdown-menu li a").click(function(){
    var selText = $(this).text();
    $(this).parents('.input-group-btn').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
});



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
    var radiusPreference = $(".dropdown-toggle").text();

    var sendInfo={
        address:userAddress,
        radius:radiusPreference
    };


    $.ajax({
        url: "http://10.194.29.0:9000/find",
        type: "post",
        dataType: "json",
        success: function (msg) {
            if (msg) {
                populateResults(msg);

            } else {
                alert("Cannot add to list !");
            }
        },
        data: sendInfo
    });

}


function populateResults(data){
    console.log(data);
}

/**
 * code for sending data from a form

 $(function(){
    $('form[name=userAddress]').submit(function(){
        $.post($(this).attr('action'), $(this).serialize(), function(json) {
           console.log(json);
        }, 'json');
        return false;
    });
});
 **/