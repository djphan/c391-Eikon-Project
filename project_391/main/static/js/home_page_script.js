var imageManager = (function(){
    return {
        // contains all image data.
        imageData: null,
        // contains a list of all groups a photo could belong to.
        groupsData: null,
        
        // holds the type of search
        searchType: null,

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
            if (this.imageData){
                return true;
            } else {
                return false;
            }
        },
        
        // populate the thumbnail grid with all available images.
        // pass in a list of image objects to populate the grid with
        populateThumbnails: function(images) {
            this.clearThumbnails();
            for (var i = 0; i < images.length; i++){
                row_container = document.createElement("div");
                row_container.className = "row";
                thumb_wrapper = document.createElement("div");
                thumb_wrapper.className = "thumbnail-wrapper";
                thumb_image = document.createElement("img");
                thumb_image.className = "thumbnail-image";
                thumb_image.src = images[i].thumbnail;
                thumb_wrapper.appendChild(thumb_image);
                row_container.appendChild(thumb_wrapper);
                // set a click listener to display as main image.
                this.thumbnailClickListener(images[i], row_container);
                // add the image to the thumbnail display
                document.getElementsByClassName("image-grid")[0].appendChild(row_container);
            }
        },
        
        // when thumbnail clicked, display as main image.
        thumbnailClickListener: function(image, clicked_element){
            _this = this;
            clicked_element.addEventListener("click", function() {
                _this.displayImage(image);
            }, 0);
        },

        // clear all thumbnails from the grid
        clearThumbnails: function() {

        },
        // displays an image 
        // pass in an image object as downloaded from server
        // to be displayed as the main image on the page.
        displayImage: function(image){
            // if no image is passed display the first image
            if (!image){
                image = this.imageData[0];
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
            if (image.editable) {
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
            }
        },

        // set the search type
        setSearchType: function(searchType) {
            this.searchType = searchType;
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
    document.getElementsByClassName("image-grid")[0].style.top = navBarHeight + "px";

    // set up tracking of search box drop down selection
    searchSelectionOptions = document.getElementsByClassName("search-options")[0].childNodes;
    for (var i = 0; i < searchSelectionOptions.length; i++){
        searchSelectionOptions[i].addEventListener("click", function(){
            // set the search type
            imageManager.setSearchType(this.dataset.searchType);
        }
    )};

    // set up the search click handler
    var searchButton = document.getElementsByClassName("search-button")[0];
    searchButton.addEventListener("click", function(){
        // Get the search query and send to 
        req.onreadystatechange=function(){
            if (req.readyState==4 && req.status == 200){
                imageManager.imageData = JSON.parse(req.responseText).images;
                imageManager.groupsData = JSON.parse(req.responseText).userGroups;
                onDataResponse();
            } else if (req.readyState==4 && req.status != 200){
                // TODO handle no search results. Either keep user images displayed or
                // clear all images.
                // swal("Could not get search image data, no images available");
            }
        };
        req.open("POST","/main/get_image_data/", true);
        // get the search terms, TODO name the search box.
        searchTerm = document.getElementsByClassName("")[0].value;
        req.setRequestHeader("Content-type", "application/json");
        req.send(JSON.stringify({searchTerm: searchTerm}));
    }, 0);
};

// called when image data has been received from server
var onDataResponse = function() {
    // display the first image
    if (imageManager.hasImages()){
        // display the first image
        imageManager.displayImage();
        imageManager.populateThumbnails(imageManager.imageData);
    }
};
// called when all image data has been received.

