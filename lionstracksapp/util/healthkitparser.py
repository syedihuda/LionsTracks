import xml.sax
import datetime

class HealthKitHandler( xml.sax.ContentHandler ):

    enums = \
    {
        "HKQuantityTypeIdentifierStepCount":"Steps",
        "HKQuantityTypeIdentifierDistanceWalkingRunning":"Distance",
        "HKQuantityTypeIdentifierFlightsClimbed":"Flights Climbed"
    }

    def __init__(self):
        self.CurrentData = ""
        self.health_data_dict_list = []

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
            datavalue = attributes["value"]
            datasource = attributes["source"]
            line.__setitem__("user", datasource)
            if datatype == "HKQuantityTypeIdentifierStepCount":
                line.__setitem__("activity_type", self.enums.get("HKQuantityTypeIdentifierStepCount"))
                #print("step count:", datavalue, "(" + attributes["unit"] + ")")
            elif datatype == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                line.__setitem__("activity_type", self.enums.get("HKQuantityTypeIdentifierDistanceWalkingRunning"))
                #print("distance walked or ran:", datavalue, "(" + attributes["unit"] + ")")
            elif datatype == "HKQuantityTypeIdentifierFlightsClimbed":
                line.__setitem__("activity_type", self.enums.get("HKQuantityTypeIdentifierFlightsClimbed"))
                #print("number of flights climbed:", datavalue, "(" + attributes["unit"] + ")")

            line.__setitem__("amount", datavalue)
            line.__setitem__("unit", attributes["unit"])
            line.__setitem__("startdatetime", attributes["startDate"])
            line.__setitem__("enddatetime", attributes["endDate"])
            doAdd = True

        if doAdd:
            self.health_data_dict_list.append(line)

    # Call when an elements ends
    def endElement(self, tag):
        pass

# if ( __name__ == "__main__"):
#     handler = HealthKitHandler()
#     handler.loadXML("C:/Users/Syed/Desktop/export/export.xml")
#     # calling parseString processes the xml as a string
#     xml.sax.parseString(str.encode(handler.getXML()), handler)
#     result = handler.get_parsed_data()
#     print(result)


    # direct example using a string
# xmlstring = \
#         "<HealthData locale=\"en_US\">" \
#         "<Record value=\"5.30647\" recordCount=\"1\" endDate=\"20150313222300-0400\" startDate=\"20150313222200-0400\" unit=\"count\" source=\"bva\" type=\"HKQuantityTypeIdentifierStepCount\"/>" \
#         "<Record value=\"13.6935\" recordCount=\"2\" endDate=\"20150313222400-0400\" startDate=\"20150313222300-0400\" unit=\"count\" source=\"bva\" type=\"HKQuantityTypeIdentifierStepCount\"/>" \
#         "<Record value=\"26.7001\" recordCount=\"3\" endDate=\"20150313222800-0400\" startDate=\"20150313222700-0400\" unit=\"count\" source=\"bva\" type=\"HKQuantityTypeIdentifierStepCount\"/>" \
#         "</HealthData>"
# handler = HealthKitHandler()
# handler.setXML(xmlstring)
# # calling parseString processes the xml as a string
# xml.sax.parseString(str.encode(handler.getXML()), handler)
# result = handler.get_parsed_data()
# print(result)



# NEED TO IMPLEMENT THIS FUNCTION
def parse_data(xmlstring):
    handler = HealthKitHandler()
    handler.setXML(xmlstring)
    # calling parseString processes the xml as a string
    xml.sax.parseString(str.encode(handler.getXML()), handler)
    return handler.get_parsed_data()

