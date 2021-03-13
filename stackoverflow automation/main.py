import pyttsx3
from subprocess import Popen, PIPE
import requests


def execute_return(cmd):
    args = cmd.split()
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err


def make_req(error):
    resp = requests.get("https://api.stackexchange.com/" +
                        "/2.2/search?order=desc&sort=activity&tagged=python&intitle={}&site=stackoverflow".format(error))
    return resp.json()


def get_urls(json_dict):
    url_list = []
    count = 0
    for i in json_dict['items']:
        if i['is_answered']:
            url_list.append(i['link'])
        count += 1
        if count == 3 or count == len(i):
            break
    import webbrowser
    for i in url_list:
        webbrowser.open(i)


if __name__ == "__main__":
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-10)
    engine.say(
        "Hey there, wait for a minute, we will get back to you if there is an error with possible solutions in stackoverflow, and for now it runs only for python script")
    engine.runAndWait()
    op, err = execute_return("python testinput.py")
    error_message = err.decode("utf-8").strip().split("\r\n")[-1]
    if error_message:
        filter_err = error_message.split(":")
        json1 = make_req(filter_err[0])
        json2 = make_req(filter_err[1])
        json3 = make_req(error_message)
        get_urls(json1)
        get_urls(json2)
        get_urls(json3)
    else:
        engine.say("Hey! There are no errors in the code")
        engine.runAndWait()
