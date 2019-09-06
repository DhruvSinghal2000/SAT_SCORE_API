from bson import ObjectId
from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask("api")
app.config['MONGO_DBNAME'] = 'myTestDB'  # connection to localdatabase
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myTestDB'

mongo = PyMongo(app)

raw_score_conversion_table = [[i for i in range(0, 59)],
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

app.url_map.strict_slashes = False


@app.route("/")
def home_page():
    """
    Welcoming Page
    :return: String
    """
    return "Welcome to test API"


@app.route('/attempts/<ObjectId:attempt_id>', methods=['GET'])
def total_score(attempt_id):
    """
    function to calculate Evidence based score for every section which is the real SAT test score
    :param attempt_id:  unique attempt id of the attempt taken by the user
    :return: dictionary containing total score and section wise score 
    """
    attempt = mongo.db.attempts  # connection to 'attempt' collection
    practice_set = mongo.db.practicesets  # connection to 'practicesets'  collection
    attempt_details = mongo.db.attemptdetails

    doc_a = attempt.find_one_or_404({'_id': ObjectId(attempt_id)})  # document of that particular ID
    doc_p = practice_set.find_one_or_404({'_id': doc_a["practicesetId"]})
    doc_atmp_d = attempt_details.find_one_or_404({'_id': doc_a["attemptdetails"]})

    questions = doc_p["questions"]  # getting all the question information from practice set document

    total_reading = 0
    total_writing = 0
    total_maths = 0

    for question in questions:  # running through all the questions in the list of all questions one by one 

        section = question["section"]
        q_id = question["question"]  # question ID

        for responses in doc_atmp_d["QA"]:
            if responses["question"] == q_id:
                if responses["obtainMarks"] == 1.0:

                    if section == "Reading Test":  # checking the section and increasing the corresponding counter
                        total_reading += 1
                    elif section == "Writing and Language":
                        total_writing += 1
                    else:
                        total_maths += 1

    reading_score = raw_score_conversion_table[2][raw_score_conversion_table[0].index(total_reading)]
    writing_score = raw_score_conversion_table[3][raw_score_conversion_table[0].index(total_writing)]
    math_score = raw_score_conversion_table[1][raw_score_conversion_table[0].index(total_maths)]

    evidence_score = (reading_score + writing_score) * 10
    total = evidence_score + math_score

    output = {"Result": {"TotalScore": total,  # creating final dictionary
                         "Section Wise Score":
                             {
                                 "ReadingTest": reading_score * 10,
                                 "Writing and Language": writing_score * 10,
                                 "Maths": math_score
                             }

                         }
              }
    return jsonify(output)


app.run(debug=True)
