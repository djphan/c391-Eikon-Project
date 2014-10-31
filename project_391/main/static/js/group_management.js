var groupManager = (function(){

    return {
        
        userGroups: null,
        getGroupInformation: function() {
            // make request for all groups and members
            // object should look like [{"groupName": "Brogrammers", "memberNames": ["Jon", "Carl", "Dan"]},... ]
            // endpoint /main/get_user_groups post {"username":"name"}
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                if (req.readyState==4 && req.status == 200){
                    this.userGroups = req.responseText;
                } else if (req.readyState==4 && req.status != 200){
                    swal("Could not get group info");
                }
            };
            req.open("POST","/main/get_user_groups", true);
            req.setRequestHeader("Content-type", "application/json");
            req.send();
            return this.userGroups;
        },

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
                // create the remove button for the element
                var removeButtonElement = document.createElement("span");
                removeButtonElement.className = "label label-danger pull-right member-remove-button";
                removeButtonElement.innerHTML = "Remove";
                var _this = this;
                removeButtonElement.addEventListener("click", function(){
                    // make request to remove
                    // on success remove on failure warn
                    swal("Remove button clicked");
                    var memberName = this.parentNode.innerHTML;
                    // you need to regex this now because you have the span tag in the html
                    _this.deleteMember(memberName, groupName);
                }, 0);
                groupMemberElement.appendChild(removeButtonElement);
                // append the created element to the list of group members
                var groupMembersElement = document.getElementsByClassName("group-members")[0];
                groupMembersElement.appendChild(groupMemberElement);
            }

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
            // make ajax request to remove
            // main/delete_user_groups post {"delete": {"group":"friends", "groupMember":"Jim"}}
            var postBody = "{'delete': {'group':" + groupName + ", groupMember:" + member + "}}";
        }
   };
})();

window.onload = function() {
    // get an array of all groups and their members
    var groupsInfo = groupManager.getGroupInformation();
    // object should look like [{"groupName": "Brogrammers", "memberNames": ["Jon", "Carl", "Dan"]},... ]
    groupsInfo = [{"groupName": "Warriors", "memberNames": ["Jon", "Jim", "Jacob", "Jason", "Jimmy", "Jill"]},
                  {"groupName": "Pets", "memberNames": ["Spot", "Speck", "Spike", "Spearmint", "Speedy", "Splash"]}];

    // Populate the groups section and
    // display the members of the first list if there is one
    if (groupsInfo) {
        groupManager.addGroupNamesToList(groupsInfo);
        groupManager.addGroupMembersToList(groupsInfo[0].members, groupsInfo[0].name); 
    }
    //groupManager.addGroupMembersToList(groupsInfo);
    groupManager.addGroupMembersToList(["Jim"], "Beep");
};
