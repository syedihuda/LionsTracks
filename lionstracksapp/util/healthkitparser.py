import xml.sax
import datetime

class HealthKitHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""

    # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "Me":
            print("-----Health Data-----")
            sex = attributes["HKCharacteristicTypeIdentifierBiologicalSex"]
            print("Sex:", sex)
            dob = attributes["HKCharacteristicTypeIdentifierDateOfBirth"]
            print("dob:", dob)
        elif tag == "ExportDate":
            print("date exported:", attributes["value"])
        elif tag == "Record":
            print("*****Record*****")
            datatype = attributes["type"]
            datavalue = attributes["value"]
            if datatype == "HKQuantityTypeIdentifierStepCount":
                print("step count:", datavalue, "(" + attributes["unit"] + ")")
            elif datatype == "HKQuantityTypeIdentifierDistanceWalkingRunning":
                print("distance walked or ran:", datavalue, "(" + attributes["unit"] + ")")
            elif datatype == "HKQuantityTypeIdentifierFlightsClimbed":
                print("number of flights climbed:", datavalue, "(" + attributes["unit"] + ")")

    # Call when an elements ends
    def endElement(self, tag):
        pass

if ( __name__ == "__main__"):
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # override the default ContextHandler
    Handler = HealthKitHandler()
    parser.setContentHandler( Handler )
    parser.parse("C:/Users/Syed/Desktop/export/export.xml")

# NEED TO IMPLEMENT THIS FUNCTION
def parse_data(data):
    #GIVEN DATA AS A STRING THAT IS IN XML FORMAT

    #RETURN DICTIONARY IN FORMAT BELOW
    health_data_dict = \
        [{'user':'Syed','activity_type':'steps','amount':200,'unit':'steps','date':datetime.datetime(2015,1,1)},
         {'user':'John','activity_type':'steps','amount':100,'unit':'steps','date':datetime.datetime(2015,1,2)}
    ]

    return health_data_dict

