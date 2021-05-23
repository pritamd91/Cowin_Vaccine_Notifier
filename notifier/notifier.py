import requests
import json
from datetime import datetime


class VaccineNotifier:

    def __init__(self):

        pass

    def get_state_id(self, state):
        """
        Function to get state id
        :param state:
        :return:
        """
        state_id = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/77.0.3865.90 Safari/537.36"}
        response = requests.get(
            "https://cdn-api.co-vin.in/api/v2/admin/location/states",
            headers=headers)
        if response.status_code is 200:
            for state_item in response.json()['states']:
                if state_item['state_name'] in state:
                    state_id = state_item['state_id']
        else:
            print("Failed on fetching state id with exception: %s" %
                  response.status_code)

        return state_id

    def get_district_id(self, state_id, district):
        """
        Function to get district id
        :param state:
        :return:
        """
        district_id = ""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/77.0.3865.90 Safari/537.36"}
        url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/{}".format(state_id)
        response = requests.get(url, headers=headers)
        if response.status_code is 200:
            for district_item in response.json()['districts']:
                if district_item['district_name'] in district:
                    district_id = district_item['district_id']
        else:
            print("Failed on fetching state id with exception: %s" %
                  response.status_code)

        return district_id

    def get_availabilityByDistrict(self, district_id, date_available):
        """
        Function to get vaccine availability based on district id & date
        :param district_id:
        :param date:
        :return:
        """
        available_data = {}
        url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public" \
              "/findByDistrict?district_id={}&date={}".format(
            district_id, date_available)
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                 "Chrome/77.0.3865.90 Safari/537.36"}
        response = requests.get(url, headers=headers)
        if response.status_code is 200:
            available_data = response.json()

        return available_data

    def get_availability(self, state, district, age_limit):
        """
        Function to get vaccine availability based on state & district name
        provided
        :param state:
        :param district:
        :return:
        """
        date_available = datetime.now().strftime('%d-%m-%Y')
        state_id = self.get_state_id(state)
        district_id = self.get_district_id(state_id, district)
        get_available = self.get_availabilityByDistrict(district_id,
                                                        date_available)
        if get_available:
            print("Available Centers for date of {}".format(str(date_available)))
            counter = 0
            for item in get_available['sessions']:
                if item['min_age_limit'] is age_limit and item[
                    'available_capacity'] > 0:
                    print("Center no: {}".format(str(counter)))
                    print("-------------------------------------------------")
                    print("Name: {}".format(item['name']))
                    print("Address: {}, {}, {}".format(item['address'],
                                                       item[
                                                           'district_name'],
                                                       item['state_name']))
                    print("Vaccine Type: {}".format(item['vaccine']))
                    print("Capacity: {}".format(item['available_capacity']))
                    print("Fee Type: {}".format(item['fee_type']))
                    counter += 1
                    print("-------------------------------------------------")


if __name__ == '__main__':
    c = VaccineNotifier()
    c.get_availability('Assam', 'Kamrup Rural', 18)