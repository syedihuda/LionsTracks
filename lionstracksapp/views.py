from time import mktime
import logging
import re
import xml.sax
import django.contrib.auth as webauth
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from lionstracksapp.forms import UserForm
import json

from django.shortcuts import render
from bs4 import BeautifulSoup

from lionstracksapp.models import HealthMetric
from lionstracksapp.util import healthkitparser_bs4

#logging.basicConfig(filename='C:/Users/John Sun/Desktop/term6/webapp/projects/healthkit/LionsTracks_3_28/LionsTracks/xml.log',level=logging.DEBUG)
logger = logging.getLogger(__name__)
user = User()

def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 'lionstracksapp/login.html', {'user_form': user_form, 'registered': registered})

# Create your views here.
def user_login(request):
    #user1 = User.objects.create_user('Jahlil','test@test.com', 'testpassword')
    #user1.last_name = 'Okafor'
    #user1.save()

    # If the request is a HTTP POST, try to pull out the relevant information.
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = User()
    # Use Django's machinery to attempt to see if the username/password
    # combination is valid - a User object is returned if it is.
    user = webauth.authenticate(username=username, password=password)

    # If we have a User object, the details are correct.
    # If None (Python's way of representing the absence of a value), no user
    # with matching credentials was found.
    if user:
        # Is the account active? It could have been disabled.
        if user.is_active:
            # If the account is valid and active, we can log the user in.
            # We'll send the user back to the homepage.
            webauth.login(request, user)
            request.session['user_id'] = user.pk
            request.session['user_name'] = user.username
            #request.session['user'] = user
            return HttpResponseRedirect('/lionstracksapp/')
            #render(request, 'lionstracksapp/dashboard.html')
        else:
            # An inactive account was used - no logging in!
            return HttpResponse("Your account is disabled.")
    else:
        # Bad login details were provided. So we can't log the user in.
        print('Invalid login details:', username, password)
        #return HttpResponse('Invalid login details supplied.' + username + ' ' + password)
        return render(request, 'lionstracksapp/login.html')

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    #return HttpResponseRedirect('/lionstracksapp/register/')
    return HttpResponseRedirect('/lionstracksapp/')

def signup(request):
    return render(request, 'lionstracksapp/signup.html', None)

def update_profile(request):
    if request.method == 'POST':
        if 'worldreadable' in request.POST: # checked
            message = 'make data public'
            user = request.session.get('user')
            profile = user.profile
            profile.world_readable = True
            profile.save()
        else:
            message = 'make data private'   # unchecked
            user = request.session.get('user')
            profile = user.profile
            profile.world_readable = False
            profile.save()
        return render(request, 'lionstracksapp/profile.html')
    else:
        return render(request, 'lionstracksapp/profile.html')

@login_required
def index(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name')
    print('index(): user_id', user_id)
    # user is not anonymous
    if user_id:
        print('index() user.id', user_id)
        context = {'step_data': '[{label:"'+user_name+'", data:'+str(get_metric_data('STEPS', user_id))+'}]',
                   'distance_data': '[{label:"'+user_name+'", data:'+str(get_metric_data('DISTANCE', user_id))+'}]',
                   'stairs_data': '[{label:"'+user_name+'", data:'+str(get_metric_data('STAIRS', user_id))+'}]',
                   'user_list': User.objects.all()}
    else:
        context = {'step_data':get_metric_data('STEPS'), 'distance_data':get_metric_data('DISTANCE'), 'stairs_data':get_metric_data('STAIRS')}
    return render(request, 'lionstracksapp/dashboard.html', context)

def show_user_metrics(request):
    user_id = request.session.get('user_id')
    # user is not anonymous
    if user_id:
        print('user.id', user_id)
        context = {'step_data':get_metric_data('STEPS', user_id), 'distance_data':get_metric_data('DISTANCE', user_id), 'stairs_data':get_metric_data('STAIRS', user_id)}
    else:
        context = {'step_data':get_metric_data('STEPS'), 'distance_data':get_metric_data('DISTANCE'), 'stairs_data':get_metric_data('STAIRS')}
    return render(request, 'lionstracksapp/dashboard.html', context)

def get_user_metrics_data(request):
    user_id = request.GET.get('userid','')
    user_name = request.GET.get('username','')
    # user is not anonymous
    if user_id:
        print('user.id', user_id)
        data = {'step_data':'{"label":"'+user_name+'", "data":'+str(get_metric_data('STEPS', user_id))+'}',
                'distance_data':'{"label":"'+user_name+'", "data":'+str(get_metric_data('DISTANCE', user_id))+'}',
                'stairs_data':'{"label":"'+user_name+'", "data":'+str(get_metric_data('STAIRS', user_id))+'}'}
    else:
        data = {'step_data':get_metric_data('STEPS'), 'distance_data':get_metric_data('DISTANCE'), 'stairs_data':get_metric_data('STAIRS')}
    return HttpResponse(json.dumps(data))

def dataupload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        handle_uploaded_file(file, request.session.get('user_id'))
        return render(request, 'lionstracksapp/dataupload.html')
    else:
        return render(request, 'lionstracksapp/dataupload.html')

def handle_uploaded_file(f, user_id):
    # user is not anonymous
    if user_id:
        print('handle_uploaded_file(): user.id', user_id)
        # Delete existing records for user
        #del_from_db('SYED')
        del_from_db(user_id)

        # Create XML File String
        xml_file_string = ''
        #for chunk in f.chunks():
        #    xml_file_string += str(chunk)
        xml_file_string = str(f.read())

        #xml_file_string = re.sub(u"[^\x20-\x7f]+",u"", xml_file_string)
        xml_cleaned = re.sub(u'[^\n\r\t\x20-\x7f]+',u'',xml_file_string)
        head = xml_cleaned.find('<?xml')
        tail = xml_cleaned.find('</HealthData>')
        xml_yea = xml_cleaned[head:tail+13]
        xml_yea2 = xml_yea.replace('\\n ','')
        xml_yea2 = xml_yea.replace('\\n','')

        logger.debug(xml_yea2)
        # Create soup from XML
        #soup = BeautifulSoup(xml_file_string)

        # Transform xml into dictionary for each metric
        #health_data_dict_steps = healthkitparser_bs4.parse_data(soup, 'SYED', 'HKQuantityTypeIdentifierStepCount', 'STEPS', 'STEPS')
        #health_data_dict_distance = healthkitparser_bs4.parse_data(soup, 'SYED', 'HKQuantityTypeIdentifierDistanceWalkingRunning', 'DISTANCE', 'MILES')
        #health_data_dict_stairs = healthkitparser_bs4.parse_data(soup, 'SYED', 'HKQuantityTypeIdentifierFlightsClimbed', 'STAIRS', 'FLIGHTS')

        handler = healthkitparser_bs4.HealthKitHandlerA()
        handler.setXML(xml_yea2)
        handler.setUser(user_id)
        # calling parseString processes the xml as a string
        xml.sax.parseString(str.encode(handler.getXML()), handler)
        health_data_dict_steps = handler.get_health_data_dict_steps()
        health_data_dict_distance = handler.get_health_data_dict_distance()
        health_data_dict_stairs = handler.get_health_data_dict_stairs()

        logger.debug(health_data_dict_steps)
        logger.debug(health_data_dict_distance)
        logger.debug(health_data_dict_stairs)

        # Save each to db
        save_to_db(health_data_dict_steps)
        save_to_db(health_data_dict_distance)
        save_to_db(health_data_dict_stairs)
    else:
        print('handle_uploaded_file(): user.id is null, anonymous can\'t upload', user_id)

def save_to_db(health_data_dict):
    for date_key in health_data_dict:
        h = HealthMetric(user=health_data_dict[date_key]['user'],
                         activity_type=health_data_dict[date_key]['activity_type'],
                         amount=health_data_dict[date_key]['amount'],
                         unit=health_data_dict[date_key]['unit'],
                         date=date_key
        )
        h.save()

def del_from_db(user_id):
    HealthMetric.objects.filter(user=str(user_id)).delete()

def get_metric_data(activity_type, user_id=-1):
    if user_id != -1:
        all_data = HealthMetric.objects.filter(activity_type=activity_type, user=str(user_id)).order_by('date').values()
    else:
        all_data = HealthMetric.objects.filter(activity_type=activity_type).order_by('date').values()
    final_result_list = []
    for item in all_data:
        final_result_list.append([mktime(item['date'].timetuple())*1000, item['amount']])
    return final_result_list



