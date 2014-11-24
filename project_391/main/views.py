import random
import calendar
from datetime import timedelta
from PIL import Image
import datetime
from django.db.models import Count, Q
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core import serializers
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, render_to_response
from main.models import Users, Persons, Session, Groups, GroupLists, Images, Views
from django.http import HttpResponse, JsonResponse
from django.forms import EmailField
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import logging
from django.shortcuts import redirect
# import pdb
import sys
import os
from project_391.settings import PROJECT_PATH
from main.datacube import generateDataCube
# Create your views here.

PUBLIC = 1 # group id for public group
PRIVATE = 2 # group id for private group

def loginPage(request):         # how do we respond to a request for a login page?

    if len(request.POST) == 0:  # "Sign In" not clicked, display log in page
        return render(request, 'main/login.html')

    # Otherwise, validate the login
    POST_username = request.POST.get('USERNAME', None)
    POST_password = request.POST.get('PASSWORD', None)
    error_msg = None

    if POST_username and POST_password:
        try:
            user = Users.objects.get(username=POST_username)
        except ObjectDoesNotExist:
            error_msg = "User %s does not exist." % POST_username
        else:
            if user.password == POST_password:
                # Send them to the index page, and store a unique sessiontracker for this session.
                response = render_to_response('main/home_page.html',
                                              {'password':POST_password, 'username':POST_username},
                                              RequestContext(request))
                st = str(hash(POST_username+str(random.random()))) # generate sessiontracker
                response.set_cookie('sessiontracker', st)                
                
                # delete any old sessions. NOTE: this means only one user account may be logged in
                # at once. we can fix this later if need be.
                Session.objects.filter(username=user).delete()
                Session.objects.create(username=user, sessiontracker=st)
                
                return response
            else:
                error_msg = "Incorrect Password, please try again."
    else:
        error_msg = "Please supply a username and password."

    error_msg = error_msg if error_msg else "Unknown Error, please report"
    return render(request, 'main/login.html', {'error_msg' : error_msg})

################################################################################

def register(request):
    if len(request.POST) == 0:  # "Register" wasn't clicked; display the empty registration page
        return render(request, 'main/register.html')

    # Get form data
    firstname       = request.POST.get('FIRSTNAME', None)
    lastname        = request.POST.get('LASTNAME', None)
    username        = request.POST.get('USERNAME', None)
    address         = request.POST.get('ADDRESS', None)
    email           = request.POST.get('EMAIL', None)
    phone           = request.POST.get('PHONE', None)
    password        = request.POST.get('PASSWORD', None)
    passwordconfirm = request.POST.get('PASSWORDCONFIRM', None)

    ### Validation ###
    err_pass_not_match = False
    err_username_taken = False

    # Check whether username already exists
    try:
        Users.objects.get(username=username)
    except ObjectDoesNotExist: # good
        pass
    else:
        err_username_taken = True

    if phone:
        # Extract just the digits from the phone number
        phone = ''.join([char for char in phone if char.isdigit()])
        # Check whether length of number falls within valid international range
        if not 8 <= len(phone) <= 15: 
            phone = None

    # Check if supplied email is a valid email address
    try:
        email = EmailField().clean(email)
    except ValidationError:
        email = None

    # Check that passwords match if both given
    if password and passwordconfirm and password != passwordconfirm:
        err_pass_not_match = True
        
    # If any fields are None (meaning not POSTed or invalid), set its
    # error variable to True, else set to False.
    err_firstname = not firstname
    err_lastname = not lastname
    err_username = not username
    err_address = not address
    err_email = not email
    err_phone = not phone
    err_password = not password
    err_passwordconfirm = not passwordconfirm

    errors = {
        "err_firstname"       : err_firstname,
        "err_lastname"        : err_lastname,
        "err_username"        : err_username,
        "err_address"         : err_address,
        "err_email"           : err_email,
        "err_phone"           : err_phone,
        "err_password"        : err_password,
        "err_passwordconfirm" : err_passwordconfirm,
        "err_pass_not_match"  : err_pass_not_match,
        "err_username_taken"  : err_username_taken
    }
        
    if any(errors.values()):
        return render(request, 'main/register.html', errors)
    else:
        # Create the newly registered user
        new_user = Users.objects.create(username=username,
                                        password=password)
        new_person = Persons.objects.create(user_name=new_user,
                                            first_name=firstname,
                                            last_name=lastname,
                                            address=address,
                                            email=email,
                                            phone=phone)

        assert new_person.user_name.password == password

        response = render_to_response('main/index.html',
                                      {'password':password, 'username':username},
                                      RequestContext(request))

        # Generate a session
        new_sessiontracker = str(hash(username+str(random.random())))
        response.set_cookie('sessiontracker', new_sessiontracker)
        
        try:
            # get the session associated with the new user
            session = Session.objects.get(username__username=username)
        except ObjectDoesNotExist: # which it shouldn't
            Session.objects.create(username=new_user,
                                   sessiontracker=new_sessiontracker)
        else:
            # set the session
            session.sessiontracker = new_sessiontracker
            session.save()

        return response
    
################################################################################

def temp_main_page(request):
    """
    Sandbox for Carl to test cookies/sessions. Beware: garbage lies below.
    """
    text = ""
    shash = request.COOKIES.get('sessiontracker', '0')
    if shash == 1:
        text += 'session tracker is marked as expired (logged out)!'
    if shash == 0:
        text += 'no \'sessiontracker\' cookie exists.'
    else:
        text += 'session tracker cookie says %s<br/>'%shash
        try:
            user = Session.objects.get(sessiontracker=shash)
        except ObjectDoesNotExist:
            text += 'no session object with that id exists in database.\n'
        else:
            text += 'this corresponds to user %s'%user
      

    return render(request, 'main/index.html', {'temp_cookie_text':text})
            
################################################################################

@csrf_exempt
def add_view(request):
    # add a view to the view count
    user = authenticate_user(request)
    try:
        # fail silently, user should not be affected by failure here
        params = json.loads(request.body)
    except:
        return HttpResponse("Failed to add view to views table", status=500)

    image = Images.objects.get(photo_id=params["photoID"])
    if image.owner_name.username == user.username:
        # exclude when users views own image.
        return HttpResponse("Users own image, view not added", status=200)

    try:
        # if the user has already viewed the image hande the exception
        Views.objects.create(photo_id=image, user_name=user)
    except IntegrityError:
        return HttpResponse("View already recorded", status=200)

    return HttpResponse("Added view to image", status=200)

@csrf_exempt
def get_olap_data(request):
    user = authenticate_user(request)
    # parse json
    # parameters passed in are the following
    params = json.loads(request.body)
    by_user = params["byUser"] #by_user True/False¬
    by_date = params["byDate"] #by_date False/weekly/monthly/yearly
    by_subject = params["bySubject"] # by_subject True/False
    start_date = params["startDate"] # start_date a date such as 2014-01-01 or False if not supplied
    end_date = params["endDate"] # end_date a date such as 2014-01-01 or False if not supplied
    # note that true false values are strings not bool

    return HttpResponse("No data", status=400) 







@csrf_exempt
def get_image_data(request):
    # This view returns all required data for displaying users images
    # and for image searches.
    # need to return thumbnail, main image, title, description, location, group, date, owner, and image_id, editable
    # also need to include a list of the users groups
    user = authenticate_user(request)
    groups = Groups.objects.all()

    # if we are returning results for a search term
    images = []
    try:
        params = json.loads(request.body)
    except:
        params = {}
    # import pdb; pdb.set_trace()
    # datetime objects are available for searches if they are set in the browser
    # note that the user can set one or both so before performing queries check
    # whether both or only one has been given by the user.
    print (params)
    if "startDate" in params:
        search_start_date = datetime.datetime.strptime(params["startDate"], "%Y-%m-%d")
    if "endDate" in params:
        search_end_date = datetime.datetime.strptime(params["endDate"], "%Y-%m-%d")

    if "searchTerm" in params:
        if params["searchTerm"] != "":
            search_term = params["searchTerm"]
            images = Images.searchByText(user, search_term)
    
    # if we are returning results for newest/oldest first search
    elif "searchType" in params:
        search_type = params["searchType"] # newest/oldest first
        allowed_groups = GroupLists.objects.filter(Q(group_id__user_name=user) | Q(friend_id=user))
        images = Images.objects.filter(Q(permitted=1) | Q(permitted=2, owner_name=user) | Q(permitted__group_id__in=[group.group_id.group_id for group in allowed_groups])).filter(timing__isnull=False)
        if search_type == "Newest":
            images = images.order_by('-timing')
        elif search_type == "Oldest":
            images = images.order_by('timing')

    # otherwise we are passing the user back all of there images
    # if the user is username 'admin' then pass them back all images
    else:
        if user.username == 'admin':
            images = Images.objects.all()
        else:
            images = Images.objects.filter(owner_name=user)

    # build the json response for each image
    response = {}
    response["images"] = []

    # if the user performed a search, append the top 5 images first
    top_image_ids = []
    if "searchType" not in params and "searchTerm" not in params:
        top_images = Views.objects.values("photo_id").annotate(Count("id")).order_by("-id__count")
        for idx, image in enumerate(top_images):
            photo_id = image["photo_id"]
            top_image = Images.objects.get(photo_id=photo_id)
            top_image = serialize_image(top_image, user)
            top_image["topImage"] = "true"
            top_image["rank"] = str(idx + 1)
            top_image["views"] = image["id__count"]
            # this handles the case where the 5th image is tied with the following images in view count.
            if idx > 4 and response["images"][idx - 1]["views"] > image["id__count"]:
                break
            response["images"].append(top_image)
            top_image_ids.append(photo_id)
    
    for image in images:
        if image.photo_id in top_image_ids:
            continue
        img = serialize_image(image, user)
        response["images"].append(img)
    
    # get all the groups the user belongs to.
    response["userGroups"] = [group.group_name + "@"  + group.user_name.username for group in Groups.objects.filter(grouplists__friend_id=user)]
    # since currently group owners aren't members we have to also add the groups they own
    user_owned_groups = [group.group_name + "@" + user.username for group in Groups.objects.filter(user_name=user)]
    response["userGroups"] = response["userGroups"] +  user_owned_groups
    response["userGroups"].append("private" + "@" + user.username)
    response["userGroups"].append("public" + "@" + user.username)
    return JsonResponse(response, status=200)


def serialize_image(image, user):
    # serializes an image object and returns it
    # top images is a list of top image photo_ids in the search
    img = {}
    img["thumbnail"] = ".." + image.thumbnail.path
    img["image"] = ".." + image.photo.path
    img["subject"] = image.subject
    img["description"] = image.description
    img["location"] = image.place

    # check whether the group is private or public and handle no username
    if image.permitted.group_name == "private" or image.permitted.group_name == "public":
        img["group"] = image.permitted.group_name + "@" + image.owner_name.username
    else:
        img["group"] = image.permitted.group_name + "@" + image.permitted.user_name.username

    if image.timing != None:
        img["date"] = image.timing.strftime("%B %d, %Y")
    else:
        img["date"] = ""

    img["owner"] = user.username
    img["imageID"] = image.photo_id
    # editable indicates whether the user can edit the details of the image.
    # if the image belongs to the user its editable.
    img["editable"] = image.owner_name.username == user.username
    return img

@csrf_exempt
def delete_image(request):
    user = authenticate_user(request)
    imageID = int(json.loads(request.body)["imageID"])
    image_to_delete = Images.objects.get(photo_id=imageID)
    image_to_delete.delete()
    return HttpResponse("Image with ID: " + str(imageID) + " deleted")

@csrf_exempt
def delete_group(request):
    user = authenticate_user(request)
    group_name_to_delete = json.loads(request.body)["groupName"]
    group = Groups.objects.get(user_name=user, group_name=group_name_to_delete)
    try:
        group.delete()
    except IntegrityError:
        return HttpResponse("Images still belong to this group. Change the groups they belong to before deleting", status=400)
    if len(Groups.objects.filter(user_name=user, group_name=group_name_to_delete)) == 0:
        return JsonResponse({"deletedGroup": group_name_to_delete}, status=200)
    else:
        return HttpResponse("Could not delete group: " + group_name_to_delete)

@csrf_exempt
def modify_image_details(request):
    user = authenticate_user(request)
    # import pdb; pdb.set_trace()    
    if request.POST["name"] == "image-subject":
        # we are editing the subject of the image.
        image = Images.objects.get(photo_id=request.POST["key"])
        image.subject = request.POST["value"]
        image.save()
        return HttpResponse("Image subject changed to " + request.POST["value"], status=200)

    if request.POST["name"] == "image-description":
        # we are editing the image description
        image = Images.objects.get(photo_id=request.POST["key"])
        image.description = request.POST["value"]
        image.save()
        return HttpResponse("Image description changed to " + request.POST["value"], status=200)

    if request.POST["name"] == "image-date":
        image = Images.objects.get(photo_id=request.POST["key"])
        # TODO format as date field before setting
        image.timing = datetime.datetime.strptime(request.POST["value"], "%Y-%m-%d")
        image.save()
        response = {}
        response["formattedDate"] = image.timing.strftime("%B %d, %Y")
        return JsonResponse(response, status=200)

    if request.POST["name"] == "image-group":
        # we are editing the image group
        # get the new group
        group_name, group_owner = request.POST["value"].split("@")
        if group_name == "private":
            new_group = Groups.objects.get(group_id=PRIVATE)
        elif group_name == "public":
            new_group = Groups.objects.get(group_id=PUBLIC)
        else:
            new_group = Groups.objects.get(user_name=group_owner,
                                group_name=group_name)
        image = Images.objects.get(photo_id=request.POST["key"])
        image.permitted = new_group
        image.save()
        return HttpResponse("Image group changed to " + request.POST["value"], status=200)

    if request.POST["name"] == "image-location":
        image = Images.objects.get(photo_id=request.POST["key"])
        image.place = request.POST["value"]
        image.save()
        return HttpResponse("Image location changed to " + request.POST["value"], status=200)
        # we are editing the image date

    else:
        return HttpResponse("Did no receive an appropriate field to edit", status=400)
    
def home_page(request):
    user = authenticate_user(request)
    if user is None:
        return redirect(loginPage)
    return render(request, 'main/home_page.html', {'username' : user.username})
        
@csrf_exempt
def upload(request):
    user = authenticate_user(request)
    if user is None:
        return redirect(loginPage)

    # get all the groups the user owns
    data = {}
    user_groups = Groups.objects.filter(user_name=user)
    data["group_names"] = [group.group_name + "@" + user.username for group in user_groups]
    # find the groups not owned by the user but that they belong to
    friend_groups = Groups.objects.filter(grouplists__friend_id=user)
    friend_groups = [group.group_name + "@" + group.user_name.username for group in friend_groups]
    # aggregate all the groups including private/public
    data["group_names"] = data["group_names"] + friend_groups
    data["group_names"].append('public' + '@' + user.username)
    data["group_names"].append('private'+ '@' + user.username)
    return render_to_response('main/uploads.html', data, 
            RequestContext(request))
    
def photo_details(request):
    user = authenticate_user(request)
    if user is None:
        return redirect(loginPage)
    return render(request, 'main/photo_details.html')
    
def group_management(request):
    user = authenticate_user(request)
    if user is None:
        return redirect(loginPage)
    return render(request, 'main/group_management.html')



#########################

@csrf_exempt
def upload_images(request):
    if not request.POST:
        return HttpResponse("Only POST requests are accepted", status=400)

    user = authenticate_user(request)
    new_image_entry = Images()
    new_image_entry.owner_name = user

    # ensure an image is attached.
    if "file" in request.FILES:
        uploaded_image = request.FILES["file"]
    else:
        return HttpResponse("No image file was provided", status=400)

    # Get the information posted with the image
    if "permissions" in request.POST:
        group_name, group_owner = request.POST["permissions"].split("@")
        if group_name == 'private': 
            new_image_entry.permitted = Groups.objects.get(group_id=PRIVATE)
        elif group_name == 'public':
            new_image_entry.permitted = Groups.objects.get(group_id=PUBLIC)
        else:
            new_image_entry.permitted = Groups.objects.get(group_name=group_name, user_name=group_owner)
    else:
        return HttpResponse("You must provide the group the image belongs to.", status=400)

    if "date" in request.POST:
        # TODO figure out whether we need to enforce a not null constraint on the date.
        # the provided create statements don't but I can't enter images with a null date.
        new_image_entry.timing = datetime.datetime.strptime(request.POST["date"], "%m/%d/%Y")

    if "location" in request.POST:
        new_image_entry.place = request.POST["location"]

    if "subject" in request.POST:
        new_image_entry.subject = request.POST["subject"]
    
    if 'description' in request.POST:
        new_image_entry.description = request.POST["description"]

    # Name confilicts are dealt with automatically
    new_image_entry.photo.save(uploaded_image.name, uploaded_image)
    new_image_entry.save()
    
    # make thumbnail
    photo_url = new_image_entry.photo.url # .../example.png
    thumb_url = photo_url[:-5] + '_thumbnail' + photo_url[-5:] # .../example.png_thumbnail.png
    make_thumbnail(photo_url, thumb_url)
    new_image_entry.thumbnail = thumb_url[7:] # [7:] cuts off the redundant "Images/" prefix
    # before saving check that both the image and thumbnail have a file path associated
    new_image_entry.save()
    if new_image_entry.photo.path and new_image_entry.thumbnail.path:
        return JsonResponse({"Image": new_image_entry.photo.url} , status=200)
    else:
        new_image_entry.delete()
        return HttpResponse("Could not save image, either the photo or the thumbnail has no image associated with it", status=500)

@csrf_exempt
def remove_user_from_group(request):
    if not request.POST:
        return HttpResponse("Only POST requests are accepted", status=400)

    # passed in {"groupMember": groupMember, "groupName":groupName}
    # to be removed from group
    # get the group
    try:
        request_body = json.loads(request.body)
        group_name = request_body["groupName"]
        group_member_to_remove = request_body["groupMember"].split(":")[0]
    except:
        return HttpResponse("Could not parse JSON object" \
                            "{'groupMember': groupMember, 'groupName':groupName}" \
                            "To remove a user from a group",
                            status=400)
    

    group = Groups.objects.get(group_name=group_name)
    user_to_remove = Users.objects.get(username=group_member_to_remove)
    group_list = GroupLists.objects.get(group_id=group, friend_id=user_to_remove)
    group_list.delete()
    return HttpResponse("The user " + group_member_to_remove + " has been deleted from " \
                            + group_name + " successfully",
                            status=200)


@csrf_exempt
def get_user_groups(request):
    # this method should pass back a list of the users groups, and a list of all usernames
    # formatted like the object below
    '''
    {"userGroups":
         [{"groupName": "Warriors", "memberNames": ["Jon", "Jim", "Jacob", "Jason", "Jimmy", "Jill"]},
         {"groupName": "Pets", "memberNames": ["Spot", "Speck", "Spike", "Spearmint", "Speedy", "Splash"]}],
     "userNames":
         ['Spot', 'Sport', 'Spill', 'Spike', 'Jack', 'Tony']
    } 
    '''

    # TODO Build an authenticate user function
    user_name = authenticate_user(request)
    # user_name = Users.objects.get(username="jonnyc") # remove this line uncomment line above once authenticate users works
    response = {}
    # look through each group of the users and find the members
    response["userGroups"] = []
    for group in Groups.objects.filter(user_name=user_name):
        group_data = {}
        group_data["groupName"] = group.group_name
        # Find the members in the group 
        group_data["memberNames"] = []
        # if the member has a notice field append it to their name for display
        for group_member in GroupLists.objects.filter(group_id=group.group_id):
            if group_member.notice:
                group_data["memberNames"].append(group_member.friend_id.username + ": " + group_member.notice)
            else:
                group_data["memberNames"].append(group_member.friend_id.username)
        response["userGroups"].append(group_data)

    # get a list of all users
    response["userNames"] = [user.username for user in Users.objects.all()]
    # TODO check for the current username in the list comprehension and remove the following line.
    response["userNames"].remove(user_name.username)
    return JsonResponse(data=response)

@csrf_exempt
def add_group(request):
    if not request.POST:
        return HttpResponse("Only POST requests can be used to add group members", status=400)

    logger = logging.getLogger(__name__)

    user_name = authenticate_user(request).username
    # user_name = Users.objects.get(username='jonnyc')

    # receives a json object {"newGroupName":"nameOfNewGroup"}
    # import pdb; pdb.set_trace()
    try:
        request_body = json.loads(request.body)
    except:
        logger.error(sys.exc_info()[0])
        return HttpResponse("Could not parse JSON add user request. \
                            new group requests should contain a request body \
                            formatted as {'newGroupName': 'nameOfNewGroup'}",
                            content_type="Apllication/json",
                            status=400)
    try:
        newGroupName = request_body["newGroupName"]
    except:
        logger.error(sys.exc_info()[0])
        return HttpResponse("Could not find property 'newGroupName' \
                            on the json request object. Ensure you pass a \
                            json object formatted like \
                            {'newGroupName': 'nameOfNewGroup'}",
                            status=400)

    # Add the group to the Groups model
    user = Users.objects.get(username=user_name)
    try:
        new_group = Groups.objects.create(user_name=user, group_name=newGroupName)
    except IntegrityError as e:
        logger.error(e)
        return HttpResponse("A Group by this name already exists", status=400)

    # Ensure group was added
    try:
        assert isinstance(Groups.objects.get(user_name=user_name, group_name=newGroupName), Groups)
    except AssertionError as e:
        logger.error(e)
        return HttpResponse("Valid request but server errored when adding group" + "\n" + e,
                            status=500)

    # Return success response
    return HttpResponse("Groups succesfully added to server: " + request.body.decode("utf-8"),
                            status=200)
@csrf_exempt       
def add_user_to_group(request):
    if not request.POST:
        return HttpResponse("Only POST requests can be used to add group members", status=400)

    logger = logging.getLogger(__name__)

    user_name = authenticate_user(request).username
    
    # receives a json object {"newGroupName":"nameOfNewGroup"}
    try:
        request_body = json.loads(request.body)
    except:
        logger.error(sys.exc_info()[0])
        return HttpResponse("Could not parse JSON. \
                            add group member requests should contain a request body \
                            formatted as \
                            {'memberName': 'member', 'groupName': 'groupName'}: ",
                            content_type="Apllication/json",
                            status=400)
    try:
        groupName = request_body["groupName"]
        memberName = request_body["memberName"]
    except:
        logger.error(sys.exc_info()[0])
        return HttpResponse("Could not find property 'groupName' or memberName \
                            on the json request object. Ensure you pass a \
                            json object formatted like: \
                            {'memberName': 'member', 'groupName': 'groupName'}",
                            status=400)

    # Get the group and user to add to it
    try:
        users_groups = Groups.objects.filter(user_name=user_name)
        group_to_add_user_to = users_groups.get(group_name=groupName)
        user_to_add = Users.objects.get(username=memberName)
    except:
        logger.error(sys.exc_info()[0]) 
        return HttpResponse("Could not add user to group" + groupName, status=500)

    try:
        if request_body["memberDescription"] != '':
            GroupLists.objects.create(friend_id=user_to_add, group_id=group_to_add_user_to, notice=request_body["memberDescription"])
        else:
            GroupLists.objects.create(friend_id=user_to_add, group_id=group_to_add_user_to)
    except IntegrityError as e:
        logger.error(e)
        return HttpResponse("This member is already part of the group: " + groupName, status=400)

    # Ensure user was added to the group list
    try:
        assert isinstance(GroupLists.objects.get(friend_id=user_to_add, group_id=group_to_add_user_to), GroupLists)
    except AssertionError as e:
        logger.error(e)
        return HttpResponse("Valid request but server errored when adding the user to the group" + "\n" + e,
                            status=500)

    # Return success response
    return HttpResponse("New member succesfully added to group: " + request.body.decode("utf-8"),
                            status=200)


def authenticate_user(request):
    st = request.COOKIES.get('sessiontracker', 'nope')
    try:
        return Session.objects.get(sessiontracker=st).username
    except ObjectDoesNotExist:
        return None

def logout(request):
    st = request.COOKIES.get('sessiontracker', '0')
    try:
        Session.objects.get(sessiontracker=st).delete()
    except ObjectDoesNotExist:
        pass
    return loginPage(request)

@csrf_exempt
def olap(request):
    user = authenticate_user(request)
    # get a list of all users
    data = {}
    data["users"] = Users.objects.all()
    return render_to_response('main/olap.html', data, 
            RequestContext(request))

# make a fixed-width thumbnail from the image at in_path and save it to out_path
def make_thumbnail(in_path, out_path):
    width = 300
    img = Image.open(PROJECT_PATH + in_path)
    scale = width / img.size[0] # by how much do we need to scale to get to <width>
    height = int(img.size[1] * scale) # determine the new height
    thumb = img.resize((width, height), Image.ANTIALIAS) # Antialias provides best scaling quality
    thumb.save(PROJECT_PATH + out_path)
    
