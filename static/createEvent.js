

function sendData(){
        console.log("function is being called");
        var eventName = $("#eventName").val();
        var address= $("#eventLocation").val();
        var description= $("#eventDescription").val();


        var dateList=$("#eventDate").val().split("-");
        var year=dateList[0];
        var month= dateList[1];
        var day=dateList[2];

        var timeList=$("#eventTime").val().split(":");
        hour=timeList[0];
        minute=timeList[1];


        var organizerName= $("#organizerName").val();
        var organizerPhone = $("#organizerPhone").val();
        var organizerEmail =  $("#organizerEmail").val();


        var sendInfo={
            name:eventName,
            description:description,
            address:address,
            year:year,
            month:month,
            day:day,
            hour:hour,
            minute:minute,
            organizer_name:organizerName,
            phone: organizerPhone,
            email:organizerEmail

        };
        console.log(sendInfo);


        $.ajax({
            url: "http://10.194.29.0:9000/create-event",
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

