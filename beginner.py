from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from bson.json_util import dumps
from pprint import pprint

app = Flask("api")
app.config['MONGO_DBNAME'] = 'myTestDB'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myTestDB'

mongo = PyMongo(app)

x = [i for i in range(0, 59)]
raw_score_conversion_table = [x,
                              [200, 200, 210, 230, 240, 260, 280, 290, 310, 320, 330, 340, 360, 370, 380, 390, 410, 420,
                               430, 440, 450, 460, 470, 480, 480, 490, 500, 510, 520, 520, 530, 540, 550, 560, 560, 570,
                               580, 590, 600, 600, 610, 620, 630, 640, 650, 660, 670, 670, 680, 690, 700, 710, 730, 740,
                               750, 760, 780, 790, 800],
                              [10, 10, 10, 11, 12, 13, 14, 15, 15, 16, 17, 17, 18, 19, 19, 20, 20, 21, 21, 22, 22, 23,
                               23, 24, 24, 25, 25, 26, 26, 27, 28, 28, 29, 29, 30, 30, 31, 31, 32, 32, 33, 33, 3, 35,
                               35, 36, 37, 37, 38, 38, 39, 40, 40],
                              [10, 10, 10, 10, 11, 12, 13, 13, 14, 15, 16, 16, 17, 18, 19, 19, 20, 21, 21, 22, 23,
                               23, 24, 25, 25, 26, 26, 27, 28, 28, 29, 30, 30, 31, 32, 32, 33, 34, 34, 35, 36, 37,
                               38, 39, 40]]


@app.route("/")
def home_page():
    return "Welcome to test API"


@app.route('/attempts/sectionTotalScore/<attempt_id>', methods=['GET'])
def get_one_attempt(attempt_id):
    attemptdet = mongo.db.attemptdetails
    practiceSet = mongo.db.practicesets
    docA = attemptdet.find_one_or_404({'_id': ObjectId(attempt_id)})
    docP = practiceSet.find_one_or_404({'_id': docA["practicesetId"]})
    questions = docP["questions"]
    totalReading = 0
    totalWriting = 0
    totalMaths = 0
    for documents in questions:
        # pprint(documents)
        section = documents["section"]
        if section == "Reading Test":
            totalReading += 1
        elif section == "Writing and Language":
            totalWriting += 1
        else:
            totalMaths += 1

    readingScore = raw_score_conversion_table[2][raw_score_conversion_table[0].index(totalReading)]
    writingScore = raw_score_conversion_table[3][raw_score_conversion_table[0].index(totalWriting)]
    mathScore = raw_score_conversion_table[1][raw_score_conversion_table[0].index(totalMaths)]

    evidenceBased = (readingScore + writingScore) * 10
    totalScore = evidenceBased + mathScore

    output = {"result": {"totalScore": totalScore,
                         "Readingtest Score": readingScore * 10,
                         "Writing and Language": writingScore * 10,
                         "Math Score": mathScore}
              }
    return dumps(output)


app.run()

# get_one_attempt("5d6be0d82931ad1966a61dc2")
