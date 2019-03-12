import unittest
import arrow
import requests


class PythonApi(unittest.TestCase):

    def test_get_measurements(self):
        utc = arrow.utcnow()
        res = requests.get('http://127.0.0.1:5000/api/v0.1/measurements')

        if res.status_code == 200:
            print("Test 'get_measurements()' PASS at " + str(utc))
        else:
            print("Test 'get_measurements()' FAIL at " + str(utc))

    def test_get_measurement(self):
        utc = arrow.utcnow()
        res = requests.get('http://127.0.0.1:5000/api/v0.1/measurement/0')

        if res.status_code == 200:
            print("Test 'get_measurement()' PASS at " + str(utc))
        else:
            print("Test 'get_measurement()' FAIL at " + str(utc))

    def test_add_measurements(self):
        utc = arrow.utcnow()

        measurement = {"date": "2019-03-10 20:50",
                        "systolic": 120,
                        "diastolic": 80
                       }

        res = requests.post('http://127.0.0.1:5000/api/v0.1/measurements', json=measurement)

        if res.status_code == 200:
            print("Test 'add_measurements()' PASS at " + str(utc))
        else:
            print("Test 'add_measurements()' FAIL at " + str(utc))

    def test_edit_measurement(self):
        utc = arrow.utcnow()

        measurement = {
                        "date": "2019-03-10 17:50",
                        "systolic": 230,
                        "diastolic": 100
                      }
        res = requests.put('http://127.0.0.1:5000/api/v0.1/measurement/1', json=measurement)
        if res.status_code == 200:
            print("Test 'edit_measurements()' PASS at " + str(utc))
        else:
            print("Test 'edit_measurements()' FAIL at " + str(utc))

    def test_delete_measurement(self):
        utc = arrow.utcnow()

        res = requests.delete('http://127.0.0.1:5000/api/v0.1/measurement/2')
        if res.status_code == 200:
            print("Test 'delete_measurements()' PASS at " + str(utc))
        else:
            print("Test 'delete_measurements()' FAIL at " + str(utc))


if __name__ == "__main__":
    unittest.main()
