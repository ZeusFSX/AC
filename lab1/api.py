from flask import Flask, jsonify, request, url_for
import arrow

app = Flask(__name__, static_url_path="")

measurements = [
    {
        "id": 0,
        "date": "2019-03-10 17:50",
        "systolic": 120,
        "diastolic": 80,
    },
    {
        "id": 1,
        "date": "2019-03-11 17:50",
        "systolic": 140,
        "diastolic": 80,
    },
]


def make_public_task(task):
    """
    Make from with id -> uri

    :param task:
    :return:
    """
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_measurement', measurement_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task


@app.route("/api/v0.1/measurements", methods=["GET"])
def get_measurements():
    """
    This function return all measurements
    0 -> http://127.0.0.1:5000/api/v0.1/measurement/0
    :return: json with measurements
    """
    return jsonify({"measurements": [i for i in map(make_public_task, measurements)]})


@app.route("/api/v0.1/measurement/<int:measurement_id>", methods=["GET"])
def get_measurement(measurement_id):
    """
    This function return measurement by id
    First find a measurement make uri for id
    and return json
    :param measurement_id: id
    :return: json
    """
    elem = list(filter(lambda t: t['id'] == measurement_id, measurements))
    if len(elem) == 0:
        return jsonify({"error": "not found"}, 404)
    return jsonify(make_public_task(measurements[measurement_id]))


@app.route("/api/v0.1/measurements", methods=["POST"])
def add_measurement():
    """
    This function add new measurement in db
    :return: json with the measurement
    """
    if "diastolic" and "systolic" not in request.json:
        return jsonify({"error": "not found"}, 404)

    measurement = {
        "id": measurements[-1]["id"] + 1,
        "systolic": request.json["systolic"],
        "diastolic": request.json["diastolic"],
        "date": request.json.get("date", arrow.now().format("YYYY-MM-DD HH:mm"))
    }
    measurements.append(measurement)
    return jsonify(make_public_task(measurement))


@app.route("/api/v0.1/measurement/<int:measurement_id>", methods=["PUT"])
def edit_measurement(measurement_id):
    """
    Edit measurement by id use
    :param measurement_id: id of element measurement
    :return: json with the measurement which was edit
    """
    elem = list(filter(lambda t: t['id'] == measurement_id, measurements))
    if len(elem) == 0:
        return jsonify({"error": "not found"}), 404

    elem[0]['systolic'] = request.json.get("systolic", elem[0]['systolic'])
    elem[0]['diastolic'] = request.json.get("diastolic", elem[0]['diastolic'])
    elem[0]["date"] = request.json.get("date", elem[0]["date"])

    return jsonify(make_public_task(elem[0]))


@app.route("/api/v0.1/measurement/<int:measurement_id>", methods=["DELETE"])
def del_measurement(measurement_id):
    """
    Delete measurement by id
    :param measurement_id: id
    :return: bool
    """
    elem = list(filter(lambda t: t['id'] == measurement_id, measurements))
    if len(elem) == 0:
        return jsonify({"error": "not found"}), 404
    measurements.remove(elem[0])
    return jsonify({"result": True})


if __name__ == '__main__':
    app.run(debug=True)
