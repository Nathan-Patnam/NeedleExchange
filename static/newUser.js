
function sendData(){
    var userEmail= $("#userEmail").val();
    var userAddress = $("#userAddress").val();
    var userRadius =  $("#userRadius").val();

    var sendInfo={

        email:userEmail,
        address:userAddress,
        radius:userRadius
    };


    $.ajax({
        url: "http://10.194.29.0:9000/create-user",
        type: "post",
        dataType: "json",
        success: function (msg) {
            if (msg) {
                console.log(msg);

            } else {
                alert("Cannot add to list !");
            }
        },
        data: sendInfo
    });
    return false;


}