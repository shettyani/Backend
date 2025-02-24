from flask import Flask, request, jsonify
import random
import datetime
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample doctor availability data with attendance tracking
doctor_schedule = {
    "Dr. Smith": {"slots": ["10:00 AM", "2:00 PM", "4:00 PM"], "attended": True},
    "Dr. Jane": {"slots": ["11:00 AM", "3:00 PM", "5:00 PM"], "attended": True}
}

# Update doctor availability
@app.route('/update_availability', methods=['POST'])
def update_availability():
    data = request.json
    doctor = data.get("doctor")
    slots = data.get("slots")
    if doctor in doctor_schedule:
        doctor_schedule[doctor]["slots"] = slots
        return jsonify({"message": "Availability updated"})
    return jsonify({"error": "Doctor not found"})

# Mark doctor attendance
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    data = request.json
    doctor = data.get("doctor")
    attended = data.get("attended")
    if doctor in doctor_schedule:
        doctor_schedule[doctor]["attended"] = attended
        return jsonify({"message": "Attendance updated"})
    return jsonify({"error": "Doctor not found"})

@app.route('/predict_availability', methods=['GET'])
def predict_availability():
    doctor = request.args.get('doctor')
    if doctor in doctor_schedule:
        if not doctor_schedule[doctor]["attended"]:
            return jsonify({"error": "Doctor did not come today"})
        return jsonify({"available_slots": doctor_schedule[doctor]["slots"]})
    return jsonify({"error": "Doctor not found"})

if __name__ == '__main__':
    app.run(debug=True)
