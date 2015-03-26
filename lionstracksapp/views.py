from time import mktime
import logging

from django.shortcuts import render
from bs4 import BeautifulSoup

from lionstracksapp.models import HealthMetric
from lionstracksapp.util import healthkitparser_bs4

logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    context = {'step_data':get_metric_data('STEPS'), 'distance_data':get_metric_data('DISTANCE'), 'stairs_data':get_metric_data('STAIRS')}
    return render(request, 'lionstracksapp/dashboard.html', context)

def dataupload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        handle_uploaded_file(file)
        return render(request, 'lionstracksapp/dataupload.html')
    else:
        return render(request, 'lionstracksapp/dataupload.html')

def handle_uploaded_file(f):
    # Delete existing records for user
    del_from_db('SYED')

    # Create XML File String
    xml_file_string = ''
    for chunk in f.chunks():
        xml_file_string += str(chunk)

    # Create soup from XML
    soup = BeautifulSoup(xml_file_string)

    # Transform xml into dictionary for each metric
    health_data_dict_steps = healthkitparser_bs4.parse_data(soup, 'SYED', 'HKQuantityTypeIdentifierStepCount', 'STEPS', 'STEPS')
    health_data_dict_distance = healthkitparser_bs4.parse_data(soup, 'SYED', 'HKQuantityTypeIdentifierDistanceWalkingRunning', 'DISTANCE', 'MILES')
    health_data_dict_stairs = healthkitparser_bs4.parse_data(soup, 'SYED', 'HKQuantityTypeIdentifierFlightsClimbed', 'STAIRS', 'FLIGHTS')

    # Save each to db
    save_to_db(health_data_dict_steps)
    save_to_db(health_data_dict_distance)
    save_to_db(health_data_dict_stairs)

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
    HealthMetric.objects.filter(user=user_id).delete()

def get_metric_data(activity_type):
    all_data = HealthMetric.objects.filter(activity_type=activity_type).order_by('date').values()
    final_result_list = []
    for item in all_data:
        final_result_list.append([mktime(item['date'].timetuple())*1000, item['amount']])
    return final_result_list



