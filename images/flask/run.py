import json
import csv
from flask import Flask, request, Response

app = Flask(__name__)

csvFilePath = './total.csv'  # csv file Path


@app.route('/GetAll', methods=['GET'])
def queryAllRecords():
    list = csv_to_json()
    return Response(response=list, status=200, mimetype='application/json')


@app.route('/GetOne', methods=['GET'])
def queryOneRecords():
    record = json.loads(request.data)
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            if record['date'] == row['date']:
                res = json.dumps(row, indent=4)
                return Response(response=res, status=200, mimetype='application/json')
    return Response(response="This date doesn't exist", status=200, mimetype='application/json')


@app.route('/Post', methods=['POST'])
def createRecord():
    record = json.loads(request.data)
    if record == {}:
        return Response(response='Error : Please provide correct data', status=400, mimetype='application/json')
    with open(csvFilePath, 'a', newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(record.values())
        f_object.close()

    return Response(response='Create successful', status=200, mimetype='application/json')


@app.route('/Delete', methods=['DELETE'])
def deleteRecord():
    record = json.loads(request.data)
    if record['date'] is None:
        return Response(response=json.dumps({"Error": "Please provide date"}),
                        status=400, mimetype='application/json')

    updatedlist = []
    isdDataExist = False

    with open(csvFilePath, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0] != record['date']:
                updatedlist.append(row)
            else:
                isdDataExist = True

    if isdDataExist:
        with open(csvFilePath, "w", newline="") as f:
            Writer = csv.writer(f)
            Writer.writerows(updatedlist)
        return Response(response="Delete successful", status=200, mimetype='application/json')
    else:
        return Response(response="The data doesn't exit", status=200, mimetype='application/json')


def csv_to_json():
    jsonArray = []

    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)

    res = json.dumps(jsonArray, indent=4)
    return res


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)
