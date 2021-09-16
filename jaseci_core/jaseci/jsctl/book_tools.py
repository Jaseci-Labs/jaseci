from jaseci.utils.utils import obj_class_cache, build_class_dict
from pprint import pformat
from inspect import getdoc
import jaseci


class book():
    def api_cheatsheet(self, root, out=None, str=""):
        if(out is None):
            out = []
        if('leaf' in root.keys()):
            out.append(str+f'& {root["leaf"][1]} &\n')
            return
        for i in root.keys():
            self.api_cheatsheet(root[i], out, str+f'{i} ')
        ret = ''
        for i in out:
            ret += i
        return ret

    def api_spec(self):
        ret = ''
        build_class_dict(jaseci)
        for i in obj_class_cache.keys():
            if(not i.endswith('_api')):
                continue
            ret += f'\\subsection{{{i[:-4]} APIs}}\n\n'
            ret += self.api_call_spec(obj_class_cache[i])
            doc = getdoc(obj_class_cache[i]).replace("\n\n", "\n\\par\n")
            doc = doc.replace('_', '\\_')
            ret += f'{doc}\n\n'
        return ret

    def api_call_spec(self, cls):
        pass
