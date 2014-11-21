var olapManager = (function(){

    return {
        // array of all user data received
        userData: [],
   
        // get all olap data for a given user
        getUserData: function(username){
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
            req.send(JSON.stringify({username: username}));
        },

        // create a chart given a usersdata
        graphUserData: function(userData, dmy){
           var data = {
              "xScale": "time",
              "yScale": "linear",
              "type": "line",
              "main": [
                {
                  "className": ".pizza",
                  "data": userData
                }]
            };
            var myChart = new xChart('line', data, '#chart'); 
        }
    };
})();


window.onload = function() {
    // set up the dates pickers
    $('#start-date').datetimepicker({pickTime: false});
    $('#end-date').datetimepicker({pickTime: false});
    // set up the user selection box
    userSelectBox = document.getElementById("user");
    userSelectBox.onchange = function(){
        userSelected = userSelectBox.options[userSelectBox.selectedIndex].text;
        olapManager.getUserData(userSelected);
    };
};
