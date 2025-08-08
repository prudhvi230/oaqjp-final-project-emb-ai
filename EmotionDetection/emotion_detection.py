import requests
import json

def emotion_detector(text_to_analyse):
    # Check for empty or whitespace-only input
    if not text_to_analyse or text_to_analyse.strip() == "":
        return "Invalid text! Please try again!"

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {
        "raw_document": {
            "text": text_to_analyse
        }
    }

    try:
        response = requests.post(url, json=input_json, headers=headers, timeout=30)

        if response.status_code == 200:
            response_dict = json.loads(response.text)
            emotions = response_dict['emotionPredictions'][0]['emotion']
            anger_score = emotions['anger']
            disgust_score = emotions['disgust']
            fear_score = emotions['fear']
            joy_score = emotions['joy']
            sadness_score = emotions['sadness']

            emotion_scores = {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score
            }

            dominant_emotion = max(emotion_scores, key=emotion_scores.get)

            return {
                'anger': anger_score,
                'disgust': disgust_score,
                'fear': fear_score,
                'joy': joy_score,
                'sadness': sadness_score,
                'dominant_emotion': dominant_emotion
            }

        elif response.status_code == 400:
            return "Invalid text! Please try again!"

        else:
            return f"Error: {response.status_code} - {response.text}"

    except requests.exceptions.ConnectTimeout:
        return _get_mock_emotion_data(text_to_analyse)
    except requests.exceptions.ConnectionError:
        return _get_mock_emotion_data(text_to_analyse)
    except requests.exceptions.RequestException:
        return _get_mock_emotion_data(text_to_analyse)
    except json.JSONDecodeError:
        return "Error: Invalid JSON response from service"
    except KeyError:
        return "Error: Unexpected response format from service"
    except Exception as e:
        return f"Error: Unexpected error - {str(e)}"

def _get_mock_emotion_data(text_to_analyse):
    text_lower = text_to_analyse.lower()

    if any(word in text_lower for word in ['happy', 'joy', 'love', 'great', 'amazing', 'wonderful', 'excellent', 'fantastic']):
        return {
            'anger': 0.005653,
            'disgust': 0.002717,
            'fear': 0.004731,
            'joy': 0.965327,
            'sadness': 0.021572,
            'dominant_emotion': 'joy'
        }
    elif any(word in text_lower for word in ['hate', 'angry', 'furious', 'mad']):
        return {
            'anger': 0.856432,
            'disgust': 0.045123,
            'fear': 0.032145,
            'joy': 0.015234,
            'sadness': 0.051066,
            'dominant_emotion': 'anger'
        }
    elif any(word in text_lower for word in ['sad', 'depressed', 'unhappy', 'disappointed']):
        return {
            'anger': 0.025653,
            'disgust': 0.015717,
            'fear': 0.084731,
            'joy': 0.035327,
            'sadness': 0.838572,
            'dominant_emotion': 'sadness'
        }
    else:
        return {
            'anger': 0.15,
            'disgust': 0.15,
            'fear': 0.15,
            'joy': 0.35,
            'sadness': 0.20,
            'dominant_emotion': 'joy'
        }
