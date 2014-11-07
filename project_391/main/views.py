import random
import datetime
from django.core import serializers
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, render_to_response
from main.models import Users, Persons, Session, Groups, GroupLists, Images
from django.http import HttpResponse, JsonResponse
from django.forms import EmailField
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import logging
# Create your views here.

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
            error_msg = "User %s does not exist." % username
        else:
            if user.password == POST_password:
                # Send them to the index page, and store a unique sessiontracker for this session.
                response = render_to_response('main/index.html',
                                              {'password':POST_password, 'username':POST_username},
                                              RequestContext(request))
                response.set_cookie('sessiontracker', str(hash(POST_username+str(random.random()))))
                # TODO store cookie in database
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
        response.set_cookie('sessiontracker', str(hash(username+str(random.random()))))
        
        try:
            session = Session.objects.get(username__username=username)
        except ObjectDoesNotExist:
            Session.objects.create(username=new_user,
                                   sessiontracker=hash(username+str(random.random())))
        else:
            session.sessiontracker=hash(username+str(random.random()))
            session.save()

        return response
    
################################################################################

def temp_main_page(request):
    """
    Sandbox for Carl to test cookies/sessions. Beware: garbage lies below.
    """
    text = ""
    shash = int(request.COOKIES.get('sessiontracker', '0'))
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

def home_page(request):
    return render(request, 'main/home_page.html')
        
def upload(request):
    return render(request, 'main/uploads.html')
    
def photo_details(request):
    return render(request, 'main/photo_details.html')
    
def group_management(request):
    return render(request, 'main/group_management.html')


@csrf_exempt
def upload_images(request):
    if not request.POST:
        return HttpResponse("Only POST requests are accepted", status=400)
    # import pdb; pdb.set_trace()
    # user_name = authenticat_user(request)
    user = Users.objects.get(username="jonnyc") # remove this line uncomment line above once authenticate users works
    new_image_entry = Images()
    new_image_entry.owner_name = user

    # ensure an image is attached.
    if "file" in request.FILES:
        uploaded_image = request.FILES["file"]
    else:
        return HttpResponse("No image file was provided", status=400)

    # Get the information posted with the image
    if "permissions" in request.POST:
        new_image_entry.permitted = Groups.objects.get(user_name=user.username, group_name=request.POST['permissions'])
    else:
        return HttpResponse("You must provide the group the image belongs to.", status=400)

    if "date" in request.POST:
        new_image_entry.timing = request.POST["date"]
    else:
        new_image_entry.timing = datetime.datetime.now()

    if "location" in request.POST:
        new_image_entry.place = request.POST["location"]

    if "subject" in request.POST:
        new_image_entry.subject = request.POST["subject"]
    
    if 'description' in request.POST:
        new_image_entry.description = request.POST["description"]

    new_image_entry.photo.save('placeholder',uploaded_image)
    # TODO resize the image for thumbnail
    new_image_entry.save()
    # pass a link back to the new image in the success response.
    return HttpResponse("Image saved", status=200)

@csrf_exempt
def remove_user_from_group(request):
    if not request.POST:
        return HttpResponse("Only POST requests are accepted", status=400)
    # user_name = authenticate_user(request)
    user_name = Users.objects.get(username="jonnyc") # remove this line uncomment line above once authenticate users works
    # passed in {"groupMember": groupMember, "groupName":groupName}
    # to be removed from group
    # get the group
    try:
        request_body = json.loads(request.body)
        group_name = request_body["groupName"]
        group_member_to_remove = request_body["groupMember"]
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
    # user_name = authenticate_user(request)
    user_name = Users.objects.get(username="jonnyc") # remove this line uncomment line above once authenticate users works
    response = {}
    # look through each group of the users and find the members
    response["userGroups"] = []
    for group in Groups.objects.filter(user_name=user_name):
        group_data = {}
        group_data["groupName"] = group.group_name
        # Find the members in the group 
        group_data["memberNames"] = [group_members.friend_id.username for 
                                group_members in GroupLists.objects.filter(group_id=group.group_id)] 
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
    # TODO Build an authenticate user function
    # user_name = authenticate_user(request).user_name
    user_name = 'jonnyc'
    # receives a json object {"newGroupName":"nameOfNewGroup"}
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
    # TODO Build an authenticate user function
    # user_name = authenticate_user(request).user_name
    user_name = 'jonnyc'
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
        new_group_list = GroupLists.objects.create(friend_id=user_to_add, group_id=group_to_add_user_to)
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
    # if user can't be authenticated
    # if authenticated 
    # return user object
    return HttpResponse("Could not authenticate")
