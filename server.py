
from flask import Flask, request, render_template
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/emotionDetector", methods=["POST"])
def emotion_detection():
    text_to_analyze = request.form["textToAnalyze"]

    result = emotion_detector(text_to_analyze)

    # Check if result is a dictionary with None (invalid or empty input)
    if isinstance(result, dict) and result.get('dominant_emotion') is None:
        return "Invalid text! Please try again!"

    # If result is an error message string
    if isinstance(result, str) and result.startswith("Error:"):
        return result

    # Format the valid emotion detection response
    response = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )

    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
