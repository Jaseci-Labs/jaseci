from jaseci.utils.utils import obj_class_cache, build_class_dict

# from pprint import pformat
from inspect import getdoc, signature
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
            line = "\\lstinline$" + str.strip()
            if root["leaf"][5]:  # cli_only
                line += " (cli only)"
            line += (
                "$ "
                + "& \\lstinline$"
                + f'{self.format_params(root["leaf"][1])}'
                + "$ \\\\ \\hline\n"
            )
            out.append(line)
            return
        for i in root.keys():
            self.api_cheatsheet(root[i], out, str + f"{i} ")
        return "".join(out)

    def get_stdlib_pre_table(self):
        clip = "\\rowcolors{1}{light-cyan}{light-gray}\\begin{longtable}{|p{4cm} | p{6cm}|}\\toprule\\rowcolor{white}\\textbf{Action}&\\textbf{Args}\\\\\\midrule"
        return clip

    def get_stdlib_post_table(self, act="default"):
        clip = (
            "\\bottomrule\\hiderowcolors\\caption{"
            + act
            + " Actions in Jac}\\label{tab:"
            + act
            + "std}\\end{longtable}"
        )
        return clip

    def std_library(self):
        import jaseci.actions.standard as stdact
        import pkgutil
        from importlib.machinery import SourceFileLoader
        from jaseci.actions.live_actions import live_actions

        all_action_sets = []
        for importer, modname, ispkg in pkgutil.iter_modules(stdact.__path__):
            all_action_sets.append(
                [modname]
                + [
                    [name, val]
                    for name, val in SourceFileLoader(
                        modname, stdact.__path__[0] + "/" + modname + ".py"
                    )
                    .load_module()
                    .__dict__.items()
                    if callable(val) and modname + "." + name in live_actions
                ]
            )
        out = []
        for i in all_action_sets:
            lib = i[0]
            if lib == "jaseci":
                continue
            out += ["\\subsection{" + lib + "}\n"]

            i = i[1:]
            for j in i:
                line = (
                    "\\apispec{"
                    + lib
                    + "."
                    + j[0]
                    + "}{"
                    + f"{self.format_params(signature(j[1]))}"
                    + "}\n"
                )
                out.append(line)
                doc = "test"  # getdoc(j[1]) if getdoc(j[1]) is not None else ""
                line = "{" + doc + "}\n"
                out.append(line)
        return "".join(out)

    def std_library_table(self):
        import jaseci.actions.standard as stdact
        import pkgutil
        from importlib.machinery import SourceFileLoader
        from jaseci.actions.live_actions import live_actions

        all_action_sets = []
        for importer, modname, ispkg in pkgutil.iter_modules(stdact.__path__):
            all_action_sets.append(
                [modname]
                + [
                    [name, val]
                    for name, val in SourceFileLoader(
                        modname, stdact.__path__[0] + "/" + modname + ".py"
                    )
                    .load_module()
                    .__dict__.items()
                    if callable(val) and modname + "." + name in live_actions
                ]
            )
        out = []
        for i in all_action_sets:
            lib = i[0]
            if lib == "jaseci":
                continue
            out += ["\subsection{" + lib + "}\n", self.get_stdlib_pre_table()]

            i = i[1:]
            for j in i:
                line = (
                    "\\lstinline$"
                    + lib
                    + "."
                    + j[0]
                    + "$ & \\lstinline$"
                    + f"{self.format_params(signature(j[1]))}"
                    + "$ \\\\ \\hline\n"
                )
                out.append(line)
                doc = getdoc(j[1]) if getdoc(j[1]) is not None else ""
                line = "\\multicolumn{2}{|p|}{Description: " + doc + "} \\\\ \\hline\n"
                out.append(line)
            out.append(self.get_stdlib_post_table(lib))
        return "".join(out)

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
