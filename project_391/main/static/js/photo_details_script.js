window.onload = function(){
    // instantiate the date time picker
    $('#datetimepicker6').datetimepicker();
    var submit_button = document.getElementClassName("submit-button")[0];
    //var form = document.getElementById("my-awesome-dropzone").style.display= "none";
    submit_button.onClick(function() {
        var location = document.getElementById("location").value;
        var subject = document.getElementById("subject").value;
        var date = document.getElementById("datetimepicker6").value;
        var permissions = document.getElementById("permissions").value;
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
};
