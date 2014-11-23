var imageManager = (function(){
    return {
        // contains all the users image files.
        imageData: null,
        
        // contains the latest searches image files
        searchImageData: null,
        
        // boolean to determine whether search results or the users
        // images are currently being displayed
        displayingSearchResults: false,
        // contains a list of all groups a photo could belong to.
        groupsData: null,
        
        // holds the type of search
        searchType: "Text",
        searchStartDate: undefined,
        searchEndDate: undefined,
        // get image information
        getImageData: function(search_terms) {
            _this = this;
            var req = new XMLHttpRequest();
            req.onreadystatechange=function(){
                if (req.readyState==4 && req.status == 200){
                    _this.imageData = JSON.parse(req.responseText).images;
                    _this.groupsData = JSON.parse(req.responseText).userGroups;
                    onDataResponse();
                } else if (req.readyState==4 && req.status != 200){
                    // swal("Could not get image data");
                }
            };
            req.open("POST","/main/get_image_data/", true);
            req.setRequestHeader("Content-type", "application/json");
            req.send();
            return;
        },

        // checks whether any images exist to display
        hasImages: function(){
            if (this.imageData.length > 0){
                return true;
            } else {
                return false;
            }
        },
        
        // populate the thumbnail grid with all available images.
        // pass in a list of image objects to populate the grid with
        // searchResultsFlag should be set to true if showing search results
        // otherwise should be set to false
        populateThumbnails: function(images, searchResultsFlag, searchTerm) {
            if (searchResultsFlag){
                this.displayingSearchResults = true;
                imageManager.displayImage(imageManager.searchImageData[0]);
                // show the search info dialog box
                imageManager.displaySearchInfo(searchTerm);
                sizeOfSearchInfo = $(".search-info").height();
                document.getElementsByClassName("image-grid")[0].style.top = 53 + sizeOfSearchInfo + "px";
            } else if (!searchResultsFlag) {
                this.displayingSearchResults = false;
                // set the height of the image grid to match to be underneath the nav bar.
                document.getElementsByClassName("image-grid")[0].style.top = 53 + "px";
            }

            this.clearThumbnails();
            for (var i = 0; i < images.length; i++){
                row_container = document.createElement("div");
                //row_container.className = "row";
                thumb_wrapper = document.createElement("div");
                thumb_wrapper.className = "thumbnail-wrapper";
                thumb_image = document.createElement("img");
                thumb_image.className = "thumbnail-image";
                thumb_image.src = images[i].thumbnail;
                thumb_wrapper.appendChild(thumb_image);
                row_container.appendChild(thumb_wrapper);
                
                // add ranking info if image is a top image
                if (images[i].topImage){
                    topTag = document.createElement("span");
                    topTag.innerHTML = "Top Image"; 
                    topTag.className = "label label-warning label-top-image";
                    thumb_wrapper.appendChild(topTag);
                    
                    /*
                    rankTag = document.createElement("span");
                    rankTag.innerHTML = "Rank: " + images[i].rank; 
                    rankTag.className = "label label-default label-rank";
                    thumb_wrapper.appendChild(rankTag);
                    */

                    viewTag = document.createElement("span");
                    viewTag.innerHTML = "Views: " + images[i].views; 
                    viewTag.className = "label label-default label-views";
                    thumb_wrapper.appendChild(viewTag);
                }
                // set a click listener to display as main image.
                this.thumbnailClickListener(images[i], row_container);
                // add the image to the thumbnail display
                document.getElementsByClassName("image-grid")[0].appendChild(row_container);
            }
            this.displayImage();
        },
        
        // when thumbnail clicked, display as main image.
        thumbnailClickListener: function(image, clicked_element){
            _this = this;
            clicked_element.addEventListener("click", function() {
                _this.displayImage(image);
                // log view
                if (!image.editable){
                    var req = new XMLHttpRequest();
                    req.open("POST","/main/add_view/", true);
                    req.setRequestHeader("Content-type", "application/json");
                    req.send(JSON.stringify({photoID: image.imageID}));
                }
            }, 0);
        },

        // clear out main image display
        clearMainImageDisplay: function() {

        },

        // clear all thumbnails from the grid
        clearThumbnails: function() {
            imageGrid = document.getElementsByClassName("image-grid")[0];
            while (imageGrid.firstChild) {
                imageGrid.removeChild(imageGrid.firstChild);
            }
        },
        // displays an image 
        // pass in an image object as downloaded from server
        // to be displayed as the main image on the page.
        displayImage: function(image){
            // if no image is passed display the first image
            if (!image){
                if (!this.displayingSearchResults){
                    // check that there is an image to display
                    if (this.imageData.length > 0){
                        image = this.imageData[0];
                    } else {
                        swal ("No images to display");
                        $(".left-side").hide();
                    }
                } else if (this.displayingSearchResults) {
                    if (this.searchImageData.length > 0){
                        image = this.searchImageData[0];
                    } else {
                        swal("No images to display");
                        $(".left-side").hide();
                    }
                }
            }

            // clear the old xeditable fields so they can be reinitialized with the
            //  new image data
            $('#image-subject').editable("destroy");
            $('#image-description').editable("destroy");
            $('#image-location').editable("destroy");
            $('#image-group').editable("destroy");
            $('#image-date').editable("destroy");

            var image_display = document.getElementsByClassName("large-image-display")[0]; 
            image_display.src = image.image;
            // place the image UID on the image div for reference
            image_display.dataset.photo_id = image.imageID;
            // set the image subject field
            var image_subject = document.getElementById("image-subject"); 
            image_subject.innerHTML = image.subject;
            // set the image description field
            var image_description = document.getElementById("image-description"); 
            image_description.innerHTML = image.description;
            // set the image location
            var image_location = document.getElementById("image-location"); 
            image_location.innerHTML = image.location;
            // set image group
            var image_group = document.getElementById("image-group"); 
            image_group.innerHTML = image.group;
            // set image date 
            var image_date = document.getElementById("image-date"); 
            image_date.innerHTML = image.date;

            // check if the image is one of the users
            // if so set up the editing functions.
            _this = this;
            deleteButton = document.getElementsByClassName("delete-button")[0]; 
            if (image.editable) {
                // insert the edit button
                //editButton = document.createElement("button");
                //editButton.type = "submit";
                //editButton.className = "delete-button btn btn-danger";
                //editButton.innerHTML = "Delete";
                //imageWrapper = document.getElementsByClassName("large-image-wrapper")[0];
                //imageWrapper.appendChild(editButton);
                classie.add(deleteButton, "editable");

                image_subject.dataset.pk = image.imageID; 
                $('#image-subject').editable({placement: "top", emptytext: "Enter a subject.",
                                            params: function(params) {
                                                data = {};
                                                data["name"] = params.name;
                                                data["value"] = params.value;
                                                data["key"] = image.imageID;
                                                return data;
                                            },

                                            success: function(response, newValue){
                                                _this.setImageData(image.imageID, "subject", newValue);
                                            }    
                                            });

                image_description.dataset.pk = image.imageID; 
                $('#image-description').editable({placement: "top", emptytext: "Enter a description.",
                                            params: function(params) {
                                                data = {};
                                                data["name"] = params.name;
                                                data["value"] = params.value;
                                                data["key"] = image.imageID;
                                                return data;
                                            },

                                            success: function(response, newValue){
                                                _this.setImageData(image.imageID, "description", newValue);
                                            }    
                                            });

                image_location.dataset.pk = image.imageID; 
                $('#image-location').editable({placement:"top", emptytext: "Enter a location.",
                                          emptyclass: "empty",
                                          params: function(params) {
                                                data = {};
                                                data["name"] = params.name;
                                                data["value"] = params.value;
                                                data["key"] = image.imageID;
                                                return data;
                                            },

                                            success: function(response, newValue){
                                                _this.setImageData(image.imageID, "location", newValue);
                                            }    
                                            });

                image_group.dataset.pk = image.imageID; 
                // create a list of groups formatted for the editable plugin
                xeditable_formatted_grouplist = [];
                for (var i = 0; i < this.groupsData.length; i++){
                    xeditable_formatted_grouplist.push({value: this.groupsData[i], text: this.groupsData[i]});
                }
                $('#image-group').editable({source: xeditable_formatted_grouplist, placement: "top", emptytext: "Select a group.",
                                            emptyclass: "empty",
                                            params: function(params) {
                                                data = {};
                                                data["name"] = params.name;
                                                data["value"] = params.value;
                                                data["key"] = image.imageID;
                                                return data;
                                            },

                                            success: function(response, newValue){
                                                _this.setImageData(image.imageID, "group", newValue);
                                            }   
                                            });
                image_date.dataset.pk = image.imageID; 
                $('#image-date').editable({placement: "top", emptytext: "Select a date.",
                                            display: false,
                                            emptyclass: "empty",
                                            params: function(params) {
                                                data = {};
                                                data["name"] = params.name;
                                                data["value"] = params.value;
                                                data["key"] = image.imageID;
                                                return data;
                                            },

                                            success: function(response, newValue){
                                                _this.setImageData(image.imageID, "date", response.formattedDate);
                                                this.innerHTML = response.formattedDate;
                                            }   
                                            });
            } else {
                classie.remove(deleteButton, "editable"); 
            }
        },

        // Search type event listener to sets the user selected search type
        addSearchTypeEventListener: function(element){
            _this = this;
            element.addEventListener("click", function() {
                imageManager.searchType = element.dataset.searchtype;
                if (imageManager.searchType === "Newest" || imageManager.searchType === "Oldest"){
                    $(".search-term").hide();
                } else {
                    $(".search-term").show();
                }
                searchButton = document.getElementsByClassName("search-button")[0];
                if (imageManager.searchType === "Text") {
                    searchButton.innerHTML = "Search: Full Text";
                } else {
                    searchButton.innerHTML = "Search:  " + element.dataset.searchtype + " First";
                }
            }, 0);
        },
        
        // Display search info shows a notification about the search
        displaySearchInfo: function(content) {
            searchResultType = document.getElementsByClassName("search-result-type")[0]; 
            if (this.searchType == "Oldest" || this.searchType == "Newest"){
                $(".search-result-type").show();
                searchResultType.innerHTML = this.searchType + " images first";
                $(".search-phrase").hide();
            } else {
                searchPhrase = document.getElementsByClassName("search-phrase")[0]; 
                $(".search-result-type").show();
                $(".search-phrase").show();
                searchPhrase.innerHTML = "\"" + content + "\"";
            }
            if (this.searchStartDate) {
                $(".search-start-date").show();
                document.getElementsByClassName("search-start-date")[0].innerHTML = "From: " + this.searchStartDate;
            } else {
                $(".search-start-date").hide();
            }
            if (this.searchEndDate) {
                $(".search-end-date").show();
                document.getElementsByClassName("search-end-date")[0].innerHTML = "To: " + this.searchEndDate;
            } else {
                $(".search-end-date").hide();
            }

        },
    
        removeObjectWithAttr: function(array, property, value){
            var index;
            // find the index of the element
            if (array === null || array === undefined) {
                return;
            }
            for (var i = 0; i < array.length; i++) {
                if (array[i][property] == value){
                    index = i;
                    array.splice(index, 1);
                    return true;
                }
            }
            // if value not found return false
            return false;
        },


        // resets a value on the stored ImageData when its changed 
        // by the user, after being updated on the server.
        setImageData: function(imageID, property, newValue) {
           for (var i = 0; i < _this.imageData.length; i++){
                if (this.imageData[i].imageID === imageID){
                    this.imageData[i][property] = newValue;
                    break;
                }
            }
        }
    };
})();
        
window.onload = function() {
    // make ajax call receive back a json array of image objects
    var jsonData = imageManager.getImageData();    
    
    // set the height of the image scrolling grid
    var navBarHeight = document.getElementById("bs-example-navbar-collapse-1").clientHeight;
    document.getElementsByClassName("image-grid")[0].style.top = 53 + "px";

    // set up date choice
    $("#dateModal").modal({show: false});
    dateChoiceSelectOption = document.getElementById("date-choice-button");
    dateChoiceSelectOption.addEventListener("click", function() {
        // launch the modal
        $("#dateModal").modal('show');
    });

    // set up date choice saving on modal close
    $("#dateModal").on('hidden.bs.modal', function() {
        // get the start and end dates
        var startDate = document.getElementById("start-date").value;
        var endDate = document.getElementById("end-date").value;
        if (startDate){
            imageManager.searchStartDate = startDate;
        } else {
            imageManager.searchStartDate = undefined;
        }
        if (endDate){
            imageManager.searchEndDate = endDate;
        } else {
            imageManager.searchEndDate = undefined;
        }
        if (startDate && endDate){
            if(new Date(startDate) > new Date(endDate)){
                swal("Date Error" ,"Start date must be before end date");
                imageManager.searchEndDate = undefined;
                $("#end-date").val("");
            }
        }
    });

    // set up tracking of search box drop down selection
    searchSelectionOptions = document.getElementsByClassName("search-option");
    for (var i = 0; i < searchSelectionOptions.length; i++){
        if (i != 3){
            imageManager.addSearchTypeEventListener(searchSelectionOptions[i]);
        }
    }
    
    // set up the delete photo button
    deletePhotoButton = document.getElementsByClassName("delete-button")[0];
    // get the image id we wanna delete
    deletePhotoButton.addEventListener("click", function(){
        var req = new XMLHttpRequest();
        var imageID = document.getElementsByClassName("large-image-display")[0].dataset.photo_id;
        req.onreadystatechange=function(){
            if (req.readyState==4 && req.status == 200){
                // remove the image thumbnail from the image grid
                imageManager.removeObjectWithAttr(imageManager.imageData, "imageID", imageID);
                imageManager.removeObjectWithAttr(imageManager.searchImageData, "imageID", imageID);
                
                // re display the thumbnails
                imageManager.clearThumbnails();
                if (imageManager.displayingSearchResults){
                    imageManager.populateThumbnails(imageManager.searchImageData, true);
                } else {
                    imageManager.populateThumbnails(imageManager.imageData, false);
                }
                
                // depending on whether we are looking at search results
                // or user data display the next image  in the large image display

            } else if (req.readyState==4 && req.status != 200){
                swal("Could not delete the image");
            }
        };
        req.open("POST","/main/delete_image/", true);
        // get the search terms, TODO name the search box.
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        req.send(JSON.stringify({imageID: imageID}));
    }, 0);
    
    // set up the button that takes users back to their own images after they
    // they have done a search.
    backToYourImages = document.getElementsByClassName("back-to-user-images")[0];
    backToYourImages.addEventListener("click", function() {
        // display the user thumbnails
        imageManager.populateThumbnails(imageManager.imageData, false, null);
    }, 0);
        
    // set up the search click handler
    var searchButton = document.getElementsByClassName("search-button")[0];
    searchButton.addEventListener("click", function(){
        searchTerm = document.getElementsByClassName("search-term")[0].value;
        if (searchTerm == "" && imageManager.searchType == "Text"){
            swal("No Search Term", "You must enter a search term.");
            return;
        }
        // Get the search query and send to 
        var req = new XMLHttpRequest();
        req.onreadystatechange=function(){
            if (req.readyState==4 && req.status == 200){
                imageManager.searchImageData = JSON.parse(req.responseText).images;
                if (imageManager.searchImageData.length > 0) {
                    imageManager.populateThumbnails(imageManager.searchImageData, true, searchTerm);
                } else {
                    swal("No Results", "We looked and looked but nothing matched your search");
                }
            } else if (req.readyState==4 && req.status != 200){
                // clear all images.
                swal("Could not get search image data from server");
            }
        };
        req.open("POST","/main/get_image_data/", true);
        req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        // if we are doing a search for all images bases on timing newest/oldest first
        var searchType = imageManager.searchType;
        var startDate = imageManager.searchStartDate;
        var endDate = imageManager.searchEndDate;
        if (searchType == "Newest" || searchType == "Oldest"){
            req.send(JSON.stringify({searchType: searchType, startDate: startDate, endDate: endDate}));
         // else we are doing a search based on timing
        } else {
            req.send(JSON.stringify({searchTerm: searchTerm, startDate: startDate, endDate: endDate}));
        }
    }, 0);
};

// called when image data has been received from server
var onDataResponse = function() {
    // display the first image
    if (imageManager.hasImages()){
        // unhide the image display elements
        $(".left-side").show();
        // and hide the upload image info
        document.getElementsByClassName("image-display")[0].style.display = "show";
        // display the first image
        imageManager.populateThumbnails(imageManager.imageData, false);
    } else {
        $(".left-side").hide();
        swal({
            title: "No Images to Display",
            text: "You have no images. Upload some?",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "Take me to your uploader.",
            cancelButtonText: "No, let me do nothing.",
            closeOnConfirm: false,   
            closeOnCancel: true
        },
        function(isConfirm){
            if(isConfirm){
                window.location.replace("/main/upload/");
            } else {
                
            }
        });

    }
};
// called when all image data has been received.

