from watson_developer_cloud import AssistantV1

watson_apikey = "KFS4CrDKubCAT5WhGHXYbX9K1zHVCrwgWhgWOBzXaVXW"
watson_url = "https://gateway-wdc.watsonplatform.net/assistant/api"
watson_workspace_id = "5f1991db-7101-4e59-835b-cb52cdeb64e9"
watson_assistant = AssistantV1(
    version = "2018-07-10",
    iam_apikey = watson_apikey,
    url = watson_url)

#TODO: fill in these functions to interface with database and client
def help_nothing(uid, text):
    return

def help_prompt(uid, text):
    return

def help_distress(uid, text):
    return

def help_cancel_distress(uid, text):
    return

def help_error(uid, text):
    return

command_table = {
    "0":help_nothing,
    "P":help_prompt,
    "D":help_distress,
    "C":help_cancel_distress,
    "E":help_error,
}

#TODO: replace these with the real server functions
watsons_contexts = {}
def server_get_context(uid):
    return watsons_contexts[uid] if uid in watsons_contexts else None

def server_set_context(uid, context):
    watsons_contexts[uid] = context
##########################

def parse_help_request(uid, text):
    response = watson_assistant.message(
        watson_workspace_id,
        input = {'text': text},
        context = server_get_context(uid)
    ).get_result()

    server_set_context(uid, response["context"])
    output_text = response["output"]["text"][0]
    command = output_text[0]
    response_speech = output_text[1:]
    command_table[command](uid, text)
    return response_speech

#TODO: remove this
uid = 0
while True:
    in_text = input(">> ")
    command_end = in_text.find(" ")
    if in_text[:command_end] == "setuid":
        uid = int(in_text[command_end+1:])
        print("set uid to %d"%(uid))
    else:
        print(parse_help_request(uid, in_text))
