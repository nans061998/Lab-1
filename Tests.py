# Tests for task_1 Litvinenko Nikita 932028

import unittest
import requests
import pytz
from datetime import datetime
from main import AppClass


class MyTestCase(unittest.TestCase):

    OK_STATUS = 200

#GET tests:

    def testEmptyGETParams(self):
        tz = pytz.timezone('GMT')
        datetime_now = datetime.now(tz)
        response_body = AppClass.HTML_TIME % {'tz': 'GMT', 'time': datetime_now.strftime(AppClass.DATETIME_FORMAT)}
        response_body_substr = response_body[:-3]
        response = requests.get('http://localhost:8000')

        self.assertEqual(response_body_substr, response.text[:-3])
        self.assertEqual(200, response.status_code)


    def testGMTGETParam(self):
        tz = pytz.timezone('GMT')
        datetime_now = datetime.now(tz)
        response_body = AppClass.HTML_TIME % {'tz': 'GMT', 'time': datetime_now.strftime(AppClass.DATETIME_FORMAT)}
        response_body_substr = response_body[:-3]
        response = requests.get('http://localhost:8000/GMT')

        self.assertEqual(response_body_substr, response.text[:-3])
        self.assertEqual(200, response.status_code)


    def testTomskGETParam(self):
        tz = pytz.timezone('Asia/Tomsk')
        datetime_now = datetime.now(tz)
        response_body = AppClass.HTML_TIME % {'tz': 'Asia/Tomsk', 'time': datetime_now.strftime(AppClass.DATETIME_FORMAT)}
        response_body_substr = response_body[:-3]
        response = requests.get('http://localhost:8000/Asia/Tomsk')

        self.assertEqual(response_body_substr, response.text[:-3])
        self.assertEqual(200, response.status_code)


    def testInvalidGETParam(self):
        response_body = AppClass.HTML_INVALID_TZ % {'tz': 'Tomsk'}
        response = requests.get('http://localhost:8000/Tomsk')

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)


# POST tests
# api/v1/convert:

    def testConvertEmptyPostParams(self):
        response_body = 'Empty request!'
        response = requests.post("http://localhost:8000/api/v1/convert")

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testConvertEmptyDateParam(self):
        response_body = "'date' POST parameter is empty!"
        target_tz = 'GMT'
        payload = {'target_tz': target_tz}
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testConvertEmptyTarget_TzParam(self):
        date_time = datetime(2021, 12, 20, 22, 21, 5)
        date_time_str = date_time.strftime(AppClass.DATETIME_FORMAT)
        tz = 'Asia/Tomsk'
        payload = {'date': '{"date":"' + date_time_str + '", "tz":"' + tz + '"}'}
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)
        response_body = "'target_tz' post parameter is empty!"

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testConvertSameTimezones(self):
        date_time = datetime(2021, 12, 20, 22, 21, 5)
        date_time_str = date_time.strftime(AppClass.DATETIME_FORMAT)
        tz = target_tz = 'EST'
        payload = {'date': '{"date":"' + date_time_str + '", "tz":"' + tz + '"}', 'target_tz': target_tz}
        response_body = "Timezones are same, date/time in '" + tz + "' is " + date_time_str
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testConvertDifferentTimezones(self):
        date_time = datetime(2021, 12, 20, 22, 21, 5)
        new_date_time = datetime(2021, 12, 20, 17, 21, 5)
        date_time_str = date_time.strftime(AppClass.DATETIME_FORMAT)
        new_date_time_str = new_date_time.strftime(AppClass.DATETIME_FORMAT)
        tz = 'GMT'
        target_tz = 'EST'
        payload = {'date': '{"date":"' + date_time_str + '", "tz":"' + tz + '"}', 'target_tz': target_tz}
        response_body = "Date/time in timezone '" + target_tz + "' is " + new_date_time_str
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidTargetTZ(self):
        date_time = datetime(2021, 12, 20, 22, 21, 5)
        date_time_str = date_time.strftime(AppClass.DATETIME_FORMAT)

        tz = 'GMT'
        target_tz = 'ES'
        payload = {'date': '{"date":"' + date_time_str + '", "tz":"' + tz + '"}', 'target_tz': target_tz}
        response_body = "Target timezone 'ES' is invalid."
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidTZ(self):
        date_time = datetime(2021, 12, 20, 22, 21, 5)
        new_date_time = datetime(2021, 12, 20, 17, 21, 5)
        date_time_str = date_time.strftime(AppClass.DATETIME_FORMAT)
        new_date_time_str = new_date_time.strftime(AppClass.DATETIME_FORMAT)
        tz = 'GM'
        target_tz = 'EST'
        payload = {'date': '{"date":"' + date_time_str + '", "tz":"' + tz + '"}', 'target_tz': target_tz}
        response_body = "Timezone 'GM' is invalid."
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidDateTime(self):
        date_time_str = "00.00.0000 00:00:00"
        tz = 'GMT'
        target_tz = 'EST'
        payload = {'date': '{"date":"' + date_time_str + '", "tz":"' + tz + '"}', 'target_tz': target_tz}
        response_body = "Date/time '00.00.0000 00:00:00' is invalid."
        response = requests.post("http://localhost:8000/api/v1/convert", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

# api/v1/datediff:

    def testDatediffEmptyPostParam(self):
        response_body = 'Empty request!'
        response = requests.post("http://localhost:8000/api/v1/datediff")

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testDatediffSameTzAndDateTimes(self):
        first_datetime = datetime(2021, 12, 20, 22, 21, 5)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime = datetime(2021, 12, 20, 22, 21, 5)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'Europe/Moscow'
        second_tz = 'Europe/Moscow'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "Dates/times and timezones are same. Difference is 0 s."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testDatediffSameTzDifferentDateTimes(self):
        first_datetime = datetime(2021, 12, 20, 22, 21, 0)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime = datetime(2021, 12, 20, 22, 21, 5)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'Europe/Moscow'
        second_tz = 'Europe/Moscow'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "Difference is 5 s."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testDatediffDifferentTzSameDateTimes(self):
        first_datetime = datetime(2021, 12, 20, 22, 21, 0)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime = datetime(2021, 12, 20, 22, 21, 0)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'Europe/Moscow'
        second_tz = 'Asia/Tomsk'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "Difference is 14400 s."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testDatediffDifferentTzAndDateTimes(self):
        first_datetime = datetime(2021, 12, 20, 20, 0, 0)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime = datetime(2021, 12, 21, 0, 0, 0)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'Europe/Moscow'
        second_tz = 'Asia/Tomsk'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "Difference is 0 s."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidFirstTZ(self):
        first_datetime = datetime(2021, 12, 20, 20, 0, 0)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime = datetime(2021, 12, 21, 0, 0, 0)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'urope/Moscow'
        second_tz = 'Asia/Tomsk'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "First timezone 'urope/Moscow' is invalid."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidSecondTZ(self):
        first_datetime = datetime(2021, 12, 20, 20, 0, 0)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime = datetime(2021, 12, 21, 0, 0, 0)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'Europe/Moscow'
        second_tz = 'Asia/Toms'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "Second timezone 'Asia/Toms' is invalid."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidFirstDateTime(self):
        first_datetime_str = "00.00.0000 00:00:00"
        second_datetime = datetime(2021, 12, 21, 0, 0, 0)
        second_datetime_str = second_datetime.strftime(AppClass.DATETIME_FORMAT)
        first_tz = 'Europe/Moscow'
        second_tz = 'Asia/Tomsk'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "First or second date/time is invalid: '00.00.0000 00:00:00', '21.12.2021 00:00:00'."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

    def testInvalidSecondDateTime(self):
        first_datetime = datetime(2021, 12, 20, 0, 0, 0)
        first_datetime_str = first_datetime.strftime(AppClass.DATETIME_FORMAT)
        second_datetime_str = "00.00.0000 00:00:00"
        first_tz = 'Europe/Moscow'
        second_tz = 'Asia/Tomsk'
        payload = {'data': '{"first_date":"' + first_datetime_str + '", "first_tz":"' + first_tz +
                           '", "second_date":"' + second_datetime_str + '", "second_tz":"' + second_tz + '"}'}
        response_body = "First or second date/time is invalid: '20.12.2021 00:00:00', '00.00.0000 00:00:00'."
        response = requests.post("http://localhost:8000/api/v1/datediff", data=payload)

        self.assertEqual(response_body, response.text)
        self.assertEqual(200, response.status_code)

if __name__ == '__main__':
    unittest.main()
