import json
from .eReturnValue import eReturnValue

def get_object_from_json_request(request, json_attributes):
    if request.content_type != 'application/json':
        raise Exception(eReturnValue.UNSUPPORTED.value)

    object_json = json.loads(request.body)
    for attribute in json_attributes:
        if attribute not in object_json:
            raise Exception(eReturnValue.NOT_SPECIFIED_NAME.value)

    return object_json

