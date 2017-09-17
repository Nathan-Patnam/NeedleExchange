

var map;

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
    map = new google.maps.Map(document.getElementById("map"), myOptions);



}


function sendAddress(){

    var userAddress =  $("#zipSearch").val();
    var sendInfo={
        address:userAddress
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
    return false;
}

function sendSubscriber(){
    var subscriberAddress =  $("#userZip").val();
    var subscriberEmail =  $("#userEmail").val();
    var sendInfo={
        address:subscriberAddress,
        email:subscriberEmail
    };
    $.ajax({
        url: "http://10.194.29.0:9000/create-user",
        type: "post",
        dataType: "json",
        success: function (msg) {
            if (msg) {
               console.log("cool");

            } else {
                alert("Cannot add to list !");
            }
        },
        data: sendInfo
    });
    return false;
}


function populateResults(data){
    console.log(data);
    $('#searchResults').empty(".eventDiv");
    var htmlString="";


    for (var i = 0; i < data.length; i++){
       htmlString+="<div class=\"eventDiv\">"+"<h4 class=\"text-center\">"+data[i].name+"</h4><address><strong>Event Location</strong><br>"+data[i].address+"<br>"+"Distance: "+data[i].dist+"km"+ "</address>"+"<strong>Organizer</strong><br>"+data[i].organizer_name+"<br>"+"Phone: "+data[i].phone+"<br>"+"Email: "+data[i].email+"<br></div>";
        var latLng = new google.maps.LatLng(data[i].lat, data[i].lng);
        var marker = new google.maps.Marker({
            position: latLng,
            map: map
        });

        if (i===0) {
            map.setZoom(15);
            map.setCenter(marker.getPosition());
        }

    }
    $('#searchResults').append(htmlString);
    return false;
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