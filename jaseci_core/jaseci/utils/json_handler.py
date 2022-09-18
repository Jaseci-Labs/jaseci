import json
from json import JSONDecoder, JSONEncoder
from uuid import UUID

from jaseci.svc import MetaService
from jaseci.utils.id_list import IdList
from jaseci.utils.utils import logger


class JaseciJsonEncoder(JSONEncoder):
    def default(self, obj):
        from jaseci.element.element import Element

        if isinstance(obj, Element):
            return {"__mem_id__": obj.id.urn}
        else:
            return super().default(obj)


class JaseciJsonDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if isinstance(obj, dict):
            if "__mem_id__" in obj:
                return self.convert(obj["__mem_id__"])
            else:
                for k in obj:
                    self.transform(obj, k)
        elif isinstance(obj, (list, tuple)):
            for idx, k in enumerate(obj):
                self.transform(obj, idx)
        return obj

    def transform(self, obj, key):
        if isinstance(obj[key], dict):
            if "__mem_id__" in obj[key]:
                obj[key] = self.convert(obj[key]["__mem_id__"])
            else:
                for k in obj[key]:
                    self.transform(obj[key], k)
        elif isinstance(obj[key], (list, tuple)):
            for idx, k in enumerate(obj[key]):
                self.transform(obj[key], idx)

    def convert(self, urn):
        return MetaService().hook().get_obj_from_store(UUID(urn))


def json_str_to_jsci_dict(input_str, parent_obj=None):
    """
    Helper function to convert JSON strings to dictionarys with _ids list
    conversions from hex to UUID

    ret_obj is the owning object for id_list objects
    """

    try:
        obj_fields = json.loads(input_str)
    except ValueError:
        logger.error(str(f"Invalid jsci_obj string {input_str} on {parent_obj.id.urn}"))
        obj_fields = {}
    for i in obj_fields.keys():
        if str(i).endswith("_ids") and isinstance(obj_fields[i], list):
            obj_fields[i] = IdList(parent_obj=parent_obj, in_list=obj_fields[i])
    return obj_fields
