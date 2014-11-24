var olapManager = (function(){

    return {
        // array of all user data received
        userData: [],
   
        // get all olap data for a given user
        getData: function(jsonParams){
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                // TODO uncomment the req.status == 200 snippet
                if (req.readyState==4 && req.status == 200){
                    olapManager.userData.push(JSON.parse(req.responseText));     
                    //olapManager.graphUserData(user
                } else if (req.readyState==4 && req.status != 200){
                    swal("Could not pull data for the user");
                }
            };
            // send post request to /main/remove_user_from_group
            // json object passed {"groupMember": groupMember, "groupName":groupName}
            req.open("POST","/main/get_olap_data/", true);
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.send(jsonParams);
        }    
    };
})();


window.onload = function() {
    // set up the user selection box
    $("#search-term").hide();
    $("#btn-group").hide();
    userSelectBox = document.getElementById("get-data-button");
    userSelectBox.addEventListener("click", function() {
        var byUser = document.getElementById("user");
        var byUser = byUser.options[byUser.selectedIndex].dataset.byuser;
        var byDate = document.getElementById("time-period");
        var byDate = byDate.options[byDate.selectedIndex].dataset.bydate;
        var bySubject = document.getElementById("subject");
        var bySubject = bySubject.options[bySubject.selectedIndex].dataset.bysubject;
        var startDate = document.getElementById("start-date").value;
        if (startDate == ""){
            startDate = "False";
        }
        var endDate = document.getElementById("end-date").value;
        if (endDate == ""){
            endDate = "False";
        }
        olapManager.getData(JSON.stringify({byUser: byUser, byDate: byDate, 
                                bySubject: bySubject, startDate: startDate, endDate: endDate}));
    });
};
