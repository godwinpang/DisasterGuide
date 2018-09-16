from watson_developer_cloud import AssistantV1
import requests
import json

watson_apikey = "KFS4CrDKubCAT5WhGHXYbX9K1zHVCrwgWhgWOBzXaVXW"
watson_url = "https://gateway-wdc.watsonplatform.net/assistant/api"
watson_workspace_id = "5f1991db-7101-4e59-835b-cb52cdeb64e9"
watson_assistant = AssistantV1(
    version = "2018-07-10",
    iam_apikey = watson_apikey,
    url = watson_url)

SERVER_HOST = "http://localhost:8088"

HEADERS = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

#TODO: fill in these functions to interface with database and client
def help_nothing(uid, text, context):
    body = {
        "user_id": uid,
        "description": text,
        "watson_context": context
    }

    try:
        return requests.post(SERVER_HOST + "/help", headers=HEADERS, data=json.dumps(body))
    except requests.exceptions.ConnectionError:
        print("ERROR: no connection could be established.")
        return {
            "success": False,
            "failure_reason": "No connection could be established."
        }

def help_prompt(uid, text, context):
    body = {
        "user_id": uid,
        "description": text,
        "watson_context": context
    }

    try:
        return requests.post(SERVER_HOST + "/help", headers=HEADERS, data=json.dumps(body))
    except requests.exceptions.ConnectionError:
        print("ERROR: no connection could be established.")
        return {
            "success": False,
            "failure_reason": "No connection could be established."
        }

def help_distress(uid, text, context):
    body = {
        "user_id": uid,
        "description": text,
        "watson_context": context,
        "distress_status": True
    }

    try:
        return requests.post(SERVER_HOST + "/help", headers=HEADERS, data=json.dumps(body))
    except requests.exceptions.ConnectionError:
        print("ERROR: no connection could be established.")
        return {
            "success": False,
            "failure_reason": "No connection could be established."
        }

def help_cancel_distress(uid, text, context):
    body = {
        "user_id": uid,
        "description": text,
        "watson_context": context,
        "distress_status": False
    }

    try:
        return requests.post(SERVER_HOST + "/help", headers=HEADERS, data=json.dumps(body))
    except requests.exceptions.ConnectionError:
        print("ERROR: no connection could be established.")
        return {
            "success": False,
            "failure_reason": "No connection could be established."
        }

def help_error(uid, text, context):
    body = {
        "user_id": uid,
        "description": text,
        "watson_context": context
    }

    try:
        return requests.post(SERVER_HOST + "/help", headers=HEADERS, data=json.dumps(body))
    except requests.exceptions.ConnectionError:
        print("ERROR: no connection could be established.")
        return {
            "success": False,
            "failure_reason": "No connection could be established."
        }

command_table = {
    "0":help_nothing,
    "P":help_prompt,
    "D":help_distress,
    "C":help_cancel_distress,
    "E":help_error,
}

def server_get_context(uid):
    body = {
        "user_id": uid
    }

    try:
        response = requests.post(SERVER_HOST + "/getwatsoncontext", headers=HEADERS, data=json.dumps(body))
        return response.json()["context"]
    except requests.exceptions.ConnectionError:
        print("ERROR: no connection could be established.")
        return None

##########################

def parse_help_request(uid, text):
    response = watson_assistant.message(
        watson_workspace_id,
        input={'text': text},
        context=server_get_context(uid)
    ).get_result()

    output_text = response["output"]["text"][0]
    command = output_text[0]
    response_speech = output_text[1:]
    command_table[command](uid, text, response["context"])
    return response_speech
