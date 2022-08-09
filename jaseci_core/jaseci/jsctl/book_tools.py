from jaseci.utils.utils import obj_class_cache, build_class_dict

# from pprint import pformat
from inspect import getdoc
import jaseci


class book:
    def format_params(self, sig):
        ret = ""
        for i in sig.parameters:
            if i == "self":
                continue
            if len(ret):
                ret += ", "
            ret += i + ": " + sig.parameters[i].annotation.__name__
            default = sig.parameters[i].default
            if default == sig.parameters[i].empty:
                ret += " (*req)"
        return ret if len(ret) else "n/a"

    def api_cheatsheet(self, root, out=None, str=""):
        if out is None:
            out = []
        if "leaf" in root.keys():
            line = "\\texttt{" + str.strip()
            if root["leaf"][5]:  # cli_only
                line += " (cli only)"
            line += (
                "} "
                + "& \\texttt{"
                + f'{self.format_params(root["leaf"][1])}'
                + "} \\\\ \\hline\n"
            )
            out.append(line)
            return
        for i in root.keys():
            self.api_cheatsheet(root[i], out, str + f"{i} ")
        ret = ""
        for i in out:
            ret += i
        return ret.replace("_", "\\_").replace("self, ", "").replace("(self)", "()")

    def api_spec(self):
        ret = ""
        build_class_dict(jaseci)
        for i in obj_class_cache.keys():
            if not i.endswith("_api"):
                continue
            ret += f"\\subsection{{{i[:-4]} APIs}}\n\n"
            doc = getdoc(obj_class_cache[i]).replace("\n\n", "\n\\par\n")
            doc = doc.replace("_", "\\_")
            ret += f"{doc}\n\n"
            ret += self.api_call_spec(obj_class_cache[i])
        return ret

    def api_call_spec(self, cls):
        ret = ""
        for i in dir(cls):
            # access = 'master'
            if i.startswith("api_"):
                api = i[4:].replace("_", " ")
            elif i.startswith("admin_api_"):
                # access = 'super'
                api = i[10:].replace("_", " ")
            elif i.startswith("public_api_"):
                # access = 'public'
                api = i[11:].replace("_", " ")
            else:
                continue
            ret += f"\\subsubsection{{{api}}}\n\n"
        return ret
