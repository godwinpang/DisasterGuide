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

def help_nothing(uid, text, context, database):
    database.log_help_call(uid, text, context)
    return True

def help_prompt(uid, text, context, database):
    database.log_help_call(uid, text, context)
    return True

def help_distress(uid, text, context, database):
    database.log_help_call(uid, text, context, True)
    return True

def help_cancel_distress(uid, text, context, database):
    database.log_help_call(uid, text, context, False)
    return True

def help_error(uid, text, context, database):
    database.log_help_call(uid, text, context)
    return True

command_table = {
    "0":help_nothing,
    "P":help_prompt,
    "D":help_distress,
    "C":help_cancel_distress,
    "E":help_error,
}

def server_get_context(uid, database):
    return database.get_watson_context(uid)

##########################

def parse_help_request(uid, text, database):
    """
    Function which is run when POST request is made to Watson API
    :param uid: UUID representing ID of user
    :param text: text transcription of user input
    :return: dictionary representing response of POST request
    """
    print("Watson received a messsage from " + str(uid) + " with message \"" + text + ".\"")
    context = server_get_context(uid, database)

    # call Watson
    response = watson_assistant.message(
        watson_workspace_id,
        input={'text': text},
        context=context
    ).get_result()

    output_text = response["output"]["text"][0]
    command = output_text[0]
    response_speech = output_text[1:]
    command_table[command](uid, text, response["context"], database)

    print("Watson responded: \"" + response_speech + ".\"")

    return {
        "success": True,
        "failure_reason": "None",
        "is_prompt": command == "P",
        "response": response_speech
    }
