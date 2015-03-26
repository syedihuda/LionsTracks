from bs4 import BeautifulSoup
import datetime

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

