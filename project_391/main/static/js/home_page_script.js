var response = {"image_list":[
    {
    "thumbnail":"http://files.softicons.com/download/system-icons/crystal-project-icons-by-everaldo-coelho/png/256x256/actions/thumbnail.png", 
    "image":"http://files.softicons.com/download/system-icons/crystal-project-icons-by-everaldo-coelho/png/256x256/actions/thumbnail.png", 
    "editable":"true", 
    "name":"Test Image", 
    "location":"Summerside"
    },

    {"thumbnail":"http://files.softicons.com/download/system-icons/crystal-project-icons-by-everaldo-coelho/png/256x256/actions/thumbnail.png", 
        "image":"http://files.softicons.com/download/system-icons/crystal-project-icons-by-everaldo-coelho/png/256x256/actions/thumbnail.png", 
        "editable":"true", 
        "name":"Test Image", 
        "location":"Summerside"
    }
]};

var dataManager = (function(){


    return {
        // create a post request and return
        // array of json objects
        getImageData: function(search_terms) {
        },
        
        createNodeObjects: function(jsonData) {
        }
    };
})();
        

$(function() {
    // make ajax call receive back a json array of image objects
    var jsonData = dataManager.getImageData();    
    // create jquery array of elements for each json object
    var nodeArray = dataManager.createNodeObjects(jsonData);
    // add the objects to the masonry grid
    var container = document.querySelector('#container');
    var msnry = new Masonry(container, {columnWidth: 100, itemSelector: '.item'});
    
    var element = $.parseHTML(
        '<div class="grid-item item center-block">' +
            '<div class="image">' +
                '<img src="./img/placeholder.jpg" class="center-block white-spacer-5 thumbnail-image-display" alt="image">' +
            '</div>'+
            '<ul class="fa-ul">' +
                '<li><i class="fa-li subject thumbnail-photo-details fa fa-comment-o"></i>Mountains</li>' +
                '<li><i class="fa-li location thumbnail-photo-details fa fa-bullseye"></i>Jasper</li>' +
                '<li><i class="fa-li group thumbnail-photo-details fa fa-group"></i>Group</li>' +
                '<li><i class="fa-li date thumbnail-photo-details fa fa-calendar-o"></i>Date</li>' +
            '</ul>' +
        '</div>');

    container.appendChild(element[0]);
    msnry.appended(element[0]);
    for (var i = 0; i < 20; i++) {
        var cloned = $(element[0]).clone();
        container.appendChild(cloned.get(0));
        msnry.appended(cloned);
    }
});
