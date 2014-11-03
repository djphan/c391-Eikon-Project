var groupManager = (function(){

    return {
        
        userGroups: null,
        userNames: null,
        getGroupInformation: function() {
            // make request for all groups and members
            // object should look like [{"groupName": "Brogrammers", "memberNames": ["Jon", "Carl", "Dan"]},... ]
            // endpoint /main/get_user_groups post {"username":"name"}
            _this = this;
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                if (req.readyState==4 && req.status == 200){
                    _this.userGroups = req.responseText;
                    return _this.userGroups;
                } else if (req.readyState==4 && req.status != 200){
                    // swal("Could not get group info");
                }
            };
            req.open("POST","/main/get_user_groups", true);
            req.setRequestHeader("Content-type", "application/json");
            req.send();
            // return this.userGroups;
            // object should look like [{"groupName": "Brogrammers", "memberNames": ["Jon", "Carl", "Dan"]},... ]
            groupsInfo = [{"groupName": "Warriors", "memberNames": ["Jon", "Jim", "Jacob", "Jason", "Jimmy", "Jill"]},
                  {"groupName": "Pets", "memberNames": ["Spot", "Speck", "Spike", "Spearmint", "Speedy", "Splash"]}];
            this.userGroups = groupsInfo;
            return this.userGroups;

        },
        // gets a list of users who can be added to groups
        // this is basically a list of all users.
        // TODO request /main/get_user_information
        getUserInformation: function(){
            _this = this;
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                if (req.readyState==4 && req.status == 200){
                    // TODO get a response object {"userNames":["Bob", "Bill", ...]}
                    _this.userNames = req.responseText;
                    // pass an array of user names to add
                    _this.setUserNames(userNameArray);
                } else if (req.readyState==4 && req.status != 200){
                    swal("Could not load user information");
                }
            };
            req.open("POST","/main/get_user_information", true);
            req.setRequestHeader("Content-type", "application/json");
            req.send();
 
        },
        // receives a array of user names to add to the select box
        setUserNames: function (arrayUserNames){
            // get the select box and populate it with the names
            var selectList = document.getElementsByClassName("user-select")[0];
            arrayUserNames.forEach(function(name) {
                var newUserNameNode = document.createElement("option");
                newUserNameNode.innerHTML = name;
                selectList.appendChild(newUserNameNode);
            });
        },
        //
        // call this function when the user creates a new group
        addNewGroupNameToList: function(groupName) {
            // first make sure we can add the group on the server
            // assuming add_group endpoint
            // TODO make sure there is not already a group by this name
            for (var i = 0; i < this.userGroups.length; i++){
                if (this.userGroups[i].groupName == groupName){
                    swal("A group by this name already exists");
                    return;
                }
            }

            // if the name is unique proceed to add it.
            _this = this;
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                if (req.readyState==4 && req.status == 200){
                    var newGroup = {"groupName": groupName, "groupMembers":[]};
                    _this.userGroups.push(newGroup);
                    _this.addGroupNamesToList([newGroup]); 
                } else if (req.readyState==4 && req.status != 200){
                    swal("Could not add group, bad response from server");
                }
            };

            // req.open("POST","/main/add_group", true);
            req.open("POST","http://requestb.in/1638wbs1");
            req.setRequestHeader("Content-type", "application/json;charset=UTF-8");
            // TODO body is not being set.
            req.send(groupName);
        },

        // call this function when adding a group that already exists to the list
        addGroupNamesToList: function(userGroups) {
            for (var i = 0; i < userGroups.length; i++){
                var groupNameElement = document.createElement("a");
                groupNameElement.className = "list-group-item";
                groupNameElement.innerHTML = userGroups[i].groupName;
                // if we need a group remove button set it here
                this.addGroupNameClickHandler(i, userGroups, groupNameElement);
                // add element to list of groups
                var groupList = document.getElementsByClassName("group-names")[0];
                groupList.appendChild(groupNameElement);
            }
        },

        addGroupNameClickHandler: function(i, userGroups, groupNameElement) {
            _this = this;
            groupNameElement.addEventListener("click", function() {
                var activeElements = groupNameElement.parentNode.getElementsByClassName("active")[0];
                for (var j = 0; j < activeElements.length; j++) {
                    classie.remove(activeElements[j], 'active');
                }
                classie.add(groupNameElement, 'active');
                _this.clearGroupMembersFromList();
                _this.addGroupMembersToList(userGroups[i].memberNames, userGroups[i].groupName);
            }, 0);
        },

        clearGroupMembersFromList: function() {
            var groupList = document.getElementsByClassName("group-members")[0];
            while (groupList.firstChild){
                groupList.removeChild(groupList.firstChild);
            }
        },

        // receives the groups name to add members from
        addGroupMembersToList: function(groupMembers, groupName) {
            // get the array of groups members based on the name
            for (var i = 0; i < groupMembers.length; i++){
                // create the main group element
                var groupMemberElement = document.createElement("a");
                groupMemberElement.className = "list-group-item";
                groupMemberElement.innerHTML = groupMembers[i];
                groupMemberElement.setAttribute("data-member-name", groupMembers[i]);
                // create the remove button for the element
                var removeButtonElement = document.createElement("span");
                removeButtonElement.className = "label label-danger pull-right member-remove-button";
                removeButtonElement.innerHTML = "Remove";
                this.deleteGroupMemberClickHandler(groupMemberElement, removeButtonElement, groupMembers, groupName);
                groupMemberElement.appendChild(removeButtonElement);
                // append the created element to the list of group members
                var groupMembersElement = document.getElementsByClassName("group-members")[0];
                groupMembersElement.appendChild(groupMemberElement);
            }
        },

        deleteGroupMemberClickHandler: function(groupMemberElement, removeButtonElement, groupMember, groupName) {
            _this = this;
            removeButtonElement.addEventListener("click", function(){
                var req = new XMLHttpRequest();
                req.onreadystatechange=function(){
                    // TODO uncomment the req.status == 200 snippet
                    if (req.readyState==4 /*req.status == 200*/){
                        _this.deleteMember(groupMember, groupName);
                        var memberName = groupMemberElement.getAttribute("data-member-name");
                        groupMemberElement.parentNode.removeChild(groupMemberElement); 

                    } else if (req.readyState==4 && req.status != 200){
                        swal("Could not remove the user from the group");
                    }
                };
                // send post request to /main/remove_user_from_group
                // json object passed {"groupMember": groupMember, "groupName":groupName}
                req.open("POST","/main/remove_user_from_group/", true);
                req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                req.send("Placeholder");
            }, 0);
        },
         
        addNewGroupMember: function(groupMember, groupName){
            // make call to attempt to add member
            // if successfull add the user to the cached group
            // and add to group list
            // otherwise display error
            if (success) {
                // find group in cached info
                var group = userGroups.filter(function(obj){return obj.groupName == groupName;});
                group.members.push(groupMember);
                addGroupMembersToList(groupMember, groupName);
            }
            if (failure) {
                swal("Failed to add member");
            }
        },
        
        deleteMember: function(member, groupName){
            // find the group that is currently active
            // TODO Ensure no groups of the same name
            var group = this.userGroups.filter(function(obj){return obj.groupName == groupName;});
            // TODO Ensure no groups with > 1 member of the same name
            group[0].memberNames.filter(function (e) { return e == member;});
        }
   };
})();

window.onload = function() {
    // get an array of all groups and their members
    var groupsInfo = groupManager.getGroupInformation();
    // get an array of all users who could be added to the list
    var getUserInfo = groupManager.getUserInformation();
    // Populate the groups section and
    // display the members of the first list if there is one
    if (groupsInfo) {
        groupManager.addGroupNamesToList(groupsInfo);
        groupManager.addGroupMembersToList(groupsInfo[0].memberNames, groupsInfo[0].groupName); 
        // show the first group as active since we show the first grouplist 
        // by default.
        var displayGroupElement = document.getElementsByClassName("group-names")[0];
        classie.add(displayGroupElement.children[0], 'active');
    }
    // set up the add group button
    var addGroupButton = document.getElementsByClassName("submit-new-group")[0];
    addGroupButton.addEventListener("click", function() {
        var groupNameTextField = document.getElementsByClassName("enter-group-name-field")[0];
        swal(groupNameTextField.value);
        groupManager.addNewGroupNameToList(groupNameTextField.value);
    });
    var addGroupSelectionBox = document.getElementsByClassName("group-select")[0];
    
    // get the select box and add a listener for when the user changes the box
    var addUserButton = document.getElementsByClassName("add-user-button")[0];
//    addUserButton.addEventListener("click", function() {
//        // get the value of the select box
//        var userSelectList = document.getElementsByClassName("user-select")[0];
//        var userNameSelected = userSelectList.options[userSelectList.selectedIndex].innerHTML;
//        // get the currently selected group name
//        var activeGroup = document.getElementsByClassName("active")[0];
//        activeGroupName = activeGroup.innerHTML;
//        // get the group members
//
//        // if they chose the "select a user option tell them to chose a name from the lsit
//        if (userSelectList.selectedIndex == 0) {
//            swal("Choose a username from the list");
//        // make sure the user isn't already in the group
//        } else if (userNameSelected in  {
};

