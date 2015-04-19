import xml.sax
import datetime
import re
from bs4 import BeautifulSoup

# parse xml, return dictionary format {date : { user, activity_type, amount, unit}}
def parse_data(soup, user_id, activity_xml_code, activity_type, unit):
    records = soup.find_all(type=activity_xml_code)
    record_dict = {}
    for record in records:
        # record_date is the key for outer dict
        record_date = datetime.datetime(int(record['startdate'][0:4]),int(record['startdate'][4:6]),int(record['startdate'][6:8]))
        # if there's an entry for record date, just increment the existing value for that day
        if record_date in record_dict:
            record_dict[record_date]['amount'] += float(record['value'])
        else: # add new record date
            record_dict[record_date] = {'user':user_id, 'activity_type':activity_type, 'amount': float(record['value']), 'unit':unit}
    return record_dict

class HealthKitHandlerA( xml.sax.ContentHandler ):

    enums = \
    {
        "HKQuantityTypeIdentifierStepCount":"Steps",
        "HKQuantityTypeIdentifierDistanceWalkingRunning":"Distance",
        "HKQuantityTypeIdentifierFlightsClimbed":"Flights Climbed"
    }

    def __init__(self):
        self.CurrentData = ""
        self.health_data_dict_list = []
        self.record_dict = {}
        self.health_data_dict_steps = {}
        self.health_data_dict_distance = {}
        self.health_data_dict_stairs = {}

    def setUser(self, user_id):
        self.user_id = str(user_id)

    def loadXML(self, file_name):
        self.fileName = file_name
        self.xmlFile = open(file_name,'r')
        self.xmlString = self.xmlFile.read()

    def getXML(self):
        return self.xmlString

    def setXML(self, xmlString):
        self.xmlString = xmlString

    def get_parsed_data(self):
        return self.health_data_dict_list

    def get_health_data_dict_steps(self):
        return self.health_data_dict_steps

    def get_health_data_dict_distance(self):
        return self.health_data_dict_distance

    def get_health_data_dict_stairs(self):
        return self.health_data_dict_stairs

    def startElement(self, tag, attributes):
        line = {}
        self.CurrentData = tag
        doAdd = False

        if tag == "Me":
            #print("-----Health Data-----")
            sex = attributes["HKCharacteristicTypeIdentifierBiologicalSex"]
            #print("Sex:", sex)
            dob = attributes["HKCharacteristicTypeIdentifierDateOfBirth"]
            #print("dob:", dob)
            doAdd = False
        elif tag == "ExportDate":
            #print("date exported:", attributes["value"])
            doAdd = False
        elif tag == "Record":
            #print("*****Record*****")
            datatype = attributes["type"]
            dataValue = attributes["value"]
            datasource = attributes["source"]
            startDate = attributes["startDate"]

            # record_date is the key for outer dict
            record_date = datetime.datetime(int(startDate[0:4]),int(startDate[4:6]),int(startDate[6:8]))

            # if there's an entry for record date, just increment the existing value for that day
            #if record_date in record_dict:
            #    record_dict[record_date]['amount'] += float(dataValue)
            #else: # add new record date
            #    record_dict[record_date] = {'user':user_id, 'activity_type':activity_type, 'amount': float(record['value']), 'unit':unit}
            #return record_dict

            if datatype == "HKQuantityTypeIdentifierStepCount":
                if record_date in self.health_data_dict_steps:
                    self.health_data_dict_steps[record_date]['amount'] += float(dataValue)
                else:
                    #self.health_data_dict_steps[record_date] = {'user':'SYED', 'activity_type':'STEPS', 'amount': float(dataValue), 'unit':'STEPS'}
                    self.health_data_dict_steps[record_date] = {'user':self.user_id, 'activity_type':'STEPS', 'amount': float(dataValue), 'unit':'STEPS'}
            elif datatype == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                if record_date in self.health_data_dict_distance:
                    self.health_data_dict_distance[record_date]['amount'] += float(dataValue)
                else:
                    #self.health_data_dict_distance[record_date] = {'user':'SYED', 'activity_type':'DISTANCE', 'amount': float(dataValue), 'unit':'MILES'}
                    self.health_data_dict_distance[record_date] = {'user':self.user_id, 'activity_type':'DISTANCE', 'amount': float(dataValue), 'unit':'MILES'}
            elif datatype == "HKQuantityTypeIdentifierFlightsClimbed":
                if record_date in self.health_data_dict_stairs:
                    self.health_data_dict_stairs[record_date]['amount'] += float(dataValue)
                else:
                    #self.health_data_dict_stairs[record_date] = {'user':'SYED', 'activity_type':'STAIRS', 'amount': float(dataValue), 'unit':'FLIGHTS'}
                    self.health_data_dict_stairs[record_date] = {'user':self.user_id, 'activity_type':'STAIRS', 'amount': float(dataValue), 'unit':'FLIGHTS'}
            doAdd = True

        if doAdd:
            self.health_data_dict_list.append(line)

    # Call when an elements ends
    def endElement(self, tag):
        pass