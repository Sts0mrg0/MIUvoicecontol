
import requests
import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone):

    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response
   

while True:

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # give the input a value
    response = recognize_speech_from_mic(recognizer, microphone)
    print("{}".format(response["transcription"]))
    try:
        brb = response["transcription"].lower() == ("be right back").lower()
        clearchat = response["transcription"].lower() == ("clear chat").lower()
        image = response["transcription"].lower() == ("image").lower()
        if brb:
            print("showing brb scene....")
            requests.post('http://localhost:8911/api/commands/{adcd1b9d-3b46-431e-8502-b36e061d017e}')
        elif clearchat:
            print("clearing chat....")
            requests.post('http://localhost:8911/api/commands/{e7ebffc8-33f1-465c-9e6e-46e964b9bf1a}')
        elif image:
            print("showing image....")
            requests.post('http://localhost:8911/api/commands/{1882efd0-d9bd-49ab-863e-00cd00700975}')
    except:
        print ('no input detected')
