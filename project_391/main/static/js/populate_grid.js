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

$(function() {

        var wall = new freewall("#grid-container");
        wall.fitWidth();
        var html = "<div class='image-grid-item'> Hello </div>";
        for (var i = 0; i < 40; i++) {
            wall.appendBlock(html);
        }
});


