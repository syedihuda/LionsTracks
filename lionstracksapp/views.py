from django.shortcuts import render
from lionstracksapp.models import HealthMetric
from lionstracksapp.util import healthkitparser
import datetime

# Create your views here.
def index(request):
    user_name = get_metric_data()
    formatted_result_list = [[18000000.0, 1], [189320400000.0, 1], [220942800000.0, 2], [284014800000.0, 2], [315550800000.0, 1], [347173200000.0, 2], [378709200000.0, 3], [410245200000.0, 3], [441781200000.0, 7], [473403600000.0, 7], [504939600000.0, 6], [536475600000.0, 3], [568011600000.0, 102], [599634000000.0, 154], [631170000000.0, 247], [662706000000.0, 285], [694242000000.0, 233], [725864400000.0, 207], [757400400000.0, 160], [788936400000.0, 200], [820472400000.0, 202], [852094800000.0, 362], [883630800000.0, 506], [915166800000.0, 545], [946702800000.0, 632], [978325200000.0, 965], [1009861200000.0, 887], [1041397200000.0, 612], [1072933200000.0, 405], [1104555600000.0, 302], [1136091600000.0, 208], [1167627600000.0, 150], [1199163600000.0, 425], [1230786000000.0, 774], [1262322000000.0, 463], [1293858000000.0, 387], [1325394000000.0, 345], [1357016400000.0, 211], [1388552400000.0, 77]];
    context = {'json_results' : formatted_result_list}
    return render(request, 'lionstracksapp/dashboard.html', context)

def dataupload(request):
    if request.method == 'POST':
        file = request.FILES['file']
        handle_uploaded_file(file)
        return render(request, 'lionstracksapp/dataupload.html')
    else:
        return render(request, 'lionstracksapp/dataupload.html')

def handle_uploaded_file(f):
    # h = HealthMetric(user='Syed',activity_type='Steps',amount=100,unit='Steps',date=datetime.datetime.now())
    # h.save()

    # Create XML File String
    xml_file_string = ''
    for chunk in f.chunks():
        xml_file_string += str(chunk)

    # Transform xml into list of dictionary
    health_data_dict = healthkitparser.parse_data(xml_file_string)

    # Save to DB
    for health_data_item in health_data_dict:
        h = HealthMetric(user=health_data_item['user'],
                         activity_type=health_data_item['activity_type'],
                         amount=health_data_item['amount'],
                         unit=health_data_item['unit'],
                         date=health_data_item['date']
        )
        h.save()

def get_metric_data():
    import datetime
    all_data = HealthMetric.objects.values()
    return all_data


