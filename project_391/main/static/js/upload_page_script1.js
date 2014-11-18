window.onload = function(){
    // instantiate the date time picker
    $('#datetimepicker6').datetimepicker({pickTime: false});
    swal("If you wish to submit photo details please place them in the fields before choosing files");
    var dropzone = window.Dropzone.instances[0];
    // set the options
    dropzone.on("sending", function(file, xhr, formData) {
        
        var location = document.getElementById("location").value;
        var subject = document.getElementById("subject").value;
        var date = document.getElementById("datetimepicker6").value;
        var permissions = document.getElementById("permissions").value;
        var description = document.getElementById("description").value;
        if (description) {
            formData.append("description", description);
        }
        if (location) {
            formData.append("location", location);
        }
        if (subject) {
            formData.append("subject", subject);
        }
        if (date) {
            formData.append("date", date);
        }
        formData.append("permissions", permissions);

    });

    dropzone.on("queuecomplete", function() {
        swal({
            title: "Upload complete",
            text: "Check out your uploaded images?",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Yes, take me to my images",
            cancelButtonText: "No, let me upload more",
            closeOnConfirm: false,   
            closeOnCancel: true
        },
        function(isConfirm){
            if(isConfirm){
                window.location.replace("/main/home/");
            } else {
                
            }
        });
});
};
