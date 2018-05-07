import json
import logging
import traceback
from datetime import date


from org.openbaton.plugin.sdk.utils import convert_from_camel_to_snake

try:
    import configparser as config_parser  # py3
except ImportError:
    import ConfigParser as config_parser  # py2

log = logging.getLogger(__name__)


class AbstractVimDriver():
    def __init__(self):
        pass

    def process_message(self, message):
        if isinstance(message, bytes):
            message = message.decode("utf-8")
        message = json.loads(message)
        params = message.get('parameters')
        method_name = convert_from_camel_to_snake(message.get('methodName'))
        log.debug("Looking for method %s" % method_name)

        method = getattr(self, method_name)
        answer = {}
        try:
            ret_obj = method(*params)
            if not ret_obj:
                return ret_obj
            if not isinstance(ret_obj, dict) and not isinstance(ret_obj, list):
                answer['answer'] = ret_obj.get_dict()
            elif isinstance(ret_obj, list):
                answer['answer'] = []
                for obj in ret_obj:
                    if type(obj) in (int, float, bool, str, date, dict):
                        answer.get('answer').append(obj)
                        #answer['answer'] = ret_obj
                        #break
                    else:
                        json_obj = obj.get_dict()
                        answer.get('answer').append(json_obj)
            else:
                answer['answer'] = ret_obj

        except Exception as e:
            traceback.print_exc()
            answer['exception'] = {'detailMessage':str(e)}
        return json.dumps(answer)

