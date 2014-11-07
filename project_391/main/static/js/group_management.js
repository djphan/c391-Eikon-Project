
var groupManager = (function(){

    return {
        
        userGroups: null,
        userNames: null,
        getGroupInformation: function() {
            // make request for all groups and members and a list of all usernames
            // object should look like {"userGroups":[{"groupName": "Brogrammers", "memberNames": ["Jon", "Carl", "Dan"]},... ], "userNames": ["jim", "jed"]}
            // endpoint /main/get_user_groups post {"username":"name"}

            _this = this;
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                if (req.readyState==4 /*&& req.status == 200*/){
                    _this.userGroups = JSON.parse(req.responseText).userGroups;
                    _this.userNames = JSON.parse(req.responseText).userNames;
                    // TODO rewrite window.onload replace with content loaded
                    onDataResponse();
                } else if (req.readyState==4 && req.status != 200){
                    // swal("Could not get group info");
                }
            };
            req.open("POST","/main/get_user_groups/", true);
            req.setRequestHeader("Content-type", "application/json");
            req.send();
                        return;

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
                    var newGroup = {"groupName": groupName, "memberNames":[]};
                    _this.userGroups.push(newGroup);
                    _this.addGroupNamesToList([newGroup]); 
                    // TODO make sure to add the new group to this.userGroups
                } else if (req.readyState==4 && req.status != 200){
                    swal("Could not add group, bad response from server" + "\n" +
                            req.responseText);
                }
            };
            
            // get the csrf token
            // var token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
            req.open("POST","/main/add_group/", true);
            // req.open("POST","http://requestb.in/1l8s2rv1");
            // req.setRequestHeader("X-CSRF-Token", token);
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.send(JSON.stringify({newGroupName: groupName}));
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
                var activeElements = groupNameElement.parentNode.getElementsByClassName("active");
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
                this.deleteGroupMemberClickHandler(groupMemberElement, removeButtonElement, groupMembers[i], groupName);
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
                        // TODO remove member from the userGroups list 
                        var group = groupManager.userGroups.filter(function(obj){ return obj.groupName == groupName;})[0];
                        var removeIndex = group.memberNames.indexOf(groupMember);
                        group.memberNames.splice(removeIndex, 1);
                        
                    } else if (req.readyState==4 && req.status != 200){
                        swal("Could not remove the user from the group");
                    }
                };
                // send post request to /main/remove_user_from_group
                // json object passed {"groupMember": groupMember, "groupName":groupName}
                req.open("POST","/main/remove_user_from_group/", true);
                req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
                req.send(JSON.stringify({groupMember: groupMember, groupName: groupName}));
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
        },

        // checks if a username is already in a given group
        addUserToGroup: function(member, groupName) {
            // get the group 
            var group = this.userGroups.filter(function(obj){return obj.groupName == groupName;})[0];
            // check if the user is already in the group
            var isMember = group.memberNames.filter(function(obj){return obj == member;});
            if (isMember.length > 0){
                swal("User is already in group");
                return;
            }
            var req = new XMLHttpRequest();
            _this = this;
            req.onreadystatechange=function(){
                if (req.readyState==4 && req.status == 200){
                    group.memberNames.push(member);
                    // update the list of users
                    _this.addGroupMembersToList([member], groupName);
                } else if (req.readyState==4 && req.status != 200){
                    swal("Could not add the user to the group");
                }
            };
            // send post request to /main/add_user_to_group
            // json object passed {"groupMember": groupMember, "groupName":groupName}
            // TODO add /main/add_user_to_group pass {"memberName":"member", "groupName":"groupName"}
            req.open("POST","/main/add_user_to_group/", true);
            req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            req.send(JSON.stringify({memberName: member, groupName: groupName}));
        },

        addUsersToSelectBox: function(userNames) {
            var addGroupSelectionBox = document.getElementsByClassName("user-select")[0];
            for (var i = 0; i < userNames.length; i++){
                var optionSelectListOptionElement = document.createElement("option");
                optionSelectListOptionElement.innerHTML = userNames[i];
                addGroupSelectionBox.appendChild(optionSelectListOptionElement);
            }
        }
   };
})();

// this gets called when the server has returned all the user
// and group information. We populate the page with the data here.
onDataResponse = function() {
    // Populate the groups section and
    // display the members of the first list if there is one
    if (groupManager.userGroups) {
        groupManager.addGroupNamesToList(groupManager.userGroups);
        // show the members of the first group
        groupManager.addGroupMembersToList(groupManager.userGroups[0].memberNames, 
                                            groupManager.userGroups[0].groupName); 
        // toggle first group as active since we show the first grouplist 
        // by default.
        var displayGroupElement = document.getElementsByClassName("group-names")[0];
        classie.add(displayGroupElement.children[0], 'active');
        // add the usernames to the select box
        groupManager.addUsersToSelectBox(groupManager.userNames);
    }

    // set up the add group button
    var addGroupButton = document.getElementsByClassName("submit-new-group")[0];
    addGroupButton.addEventListener("click", function() {
        var groupNameTextField = document.getElementsByClassName("enter-group-name-field")[0];
        groupManager.addNewGroupNameToList(groupNameTextField.value);
    });
    var addGroupSelectionBox = document.getElementsByClassName("group-select")[0];
    
    // set up the add button
    var addUserButton = document.getElementsByClassName("add-user-button")[0];
    addUserButton.addEventListener("click", function() {
        // get the value of the select box
        var userSelectList = document.getElementsByClassName("user-select")[0];
        var userNameSelected = userSelectList.options[userSelectList.selectedIndex].innerHTML;
        // get the currently selected group name
        var groupList = document.getElementsByClassName("group-names")[0];
        var activeGroup = groupList.getElementsByClassName("active")[0];
        activeGroupName = activeGroup.innerHTML;
        groupManager.addUserToGroup(userNameSelected, activeGroupName);
    });
};

window.onload = function(){
    // get an array of all groups and their members and all users
    groupManager.getGroupInformation();
};
