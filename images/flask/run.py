from argparse import FileType
import json
import csv
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

PredFilePath = './Pred.csv'  # csv file Path
GroundTruthFilePath = './GroundTruth.csv'

@app.route('/')
@app.route('/Probe')
def probe():
    return 'hello!'

@app.route('/GetAll/<string:FileName>', methods=['GET'])
def queryAllRecords(FileName):
    csvFilePath = getCSVFilePath(FileName)
    if csvFilePath == "error":
        return Response(response="Please provide correct file name", status=400, mimetype='application/json')

    list = csv_to_json(csvFilePath)
    return Response(response=list, status=200, mimetype='application/json')


@app.route('/GetOne/<string:FileName>', methods=['GET'])
def queryOneRecords(FileName):
    csvFilePath = getCSVFilePath(FileName)
    if csvFilePath == "error":
        return Response(response="Please provide correct file name", status=400, mimetype='application/json')

    record = json.loads(request.data)
    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            if record['date'] == row['date']:
                res = json.dumps(row, indent=4)
                return Response(response=res, status=200, mimetype='application/json')
    return Response(response="This date doesn't exist", status=400, mimetype='application/json')


@app.route('/Post/<string:FileName>', methods=['POST'])
def createRecord(FileName):
    csvFilePath = getCSVFilePath(FileName)
    if csvFilePath == "error":
        return Response(response="Please provide correct file name", status=400, mimetype='application/json')

    record = json.loads(request.data)
    if record == {}:
        return Response(response='Error : Please provide correct data', status=400, mimetype='application/json')
    with open(csvFilePath, 'a', newline='') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(record.values())
        f_object.close()

    return Response(response='Create successful', status=200, mimetype='application/json')


@app.route('/Delete/<string:FileName>', methods=['DELETE'])
def deleteRecord(FileName):
    csvFilePath = getCSVFilePath(FileName)
    if csvFilePath == "error":
        return Response(response="Please provide correct file name", status=400, mimetype='application/json')

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


def csv_to_json(csvFilePath):
    jsonArray = []

    with open(csvFilePath, encoding='utf-8-sig') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            jsonArray.append(row)

    res = json.dumps(jsonArray, indent=4)
    return res


def getCSVFilePath(FileName):
    if FileName == "P":
        return PredFilePath
    elif FileName == "G":
        return GroundTruthFilePath
    else:
        return "error"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
