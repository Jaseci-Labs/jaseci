from jaseci.utils.utils import obj_class_cache, build_class_dict
from jaseci.prim.super_master import SuperMaster as Sm
from docstring_parser import parse
from os.path import exists

# from pprint import pformat
from inspect import getdoc, signature
import jaseci


class Book:
    def format_params(self, sig, ignore_args=[]):
        ret = ""
        for i in sig.parameters:
            if i == "self" or i in ignore_args:
                continue
            if len(ret):
                ret += ", "
            ret += i + ": " + sig.parameters[i].annotation.__name__
            default = sig.parameters[i].default
            if default == sig.parameters[i].empty:
                ret += " (*req)"
            else:
                # if isinstance(default, str):
                #     default = default.encode("unicode_escape").lstrip("b")
                default = (
                    str(default)
                    .replace("_", "\\_")
                    .replace("{", "\\{")
                    .replace("}", "\\}")
                    .replace("\n", "\\\\n")
                )
                ret += f" ({default})"
        return ret if len(ret) else "n/a"

    def bookgen_api_cheatsheet(self, root, out=None, str=""):
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
            self.bookgen_api_cheatsheet(root[i], out, str + f"{i} ")
        return "".join(out)

    def get_stdlib_pre_table(self):
        clip = (
            "\\rowcolors{1}{light-cyan}{light-gray}\\begin{longtable}"
            "{|p{4cm} | p{6cm}|}\\toprule\\rowcolor{white}\\textbf"
            "{Action}&\\textbf{Args}\\\\\\midrule"
        )
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

    def get_global_actions(self):
        import jaseci.extens.act_lib as stdact
        import pkgutil
        from importlib.machinery import SourceFileLoader
        from jaseci.jsorc.live_actions import live_actions

        all_action_sets = []
        for importer, modname, ispkg in pkgutil.iter_modules(stdact.__path__):
            if not exists(stdact.__path__[0] + "/" + modname + ".py"):
                continue
            mod = SourceFileLoader(
                modname, stdact.__path__[0] + "/" + modname + ".py"
            ).load_module()
            all_action_sets.append(
                [modname]
                + [getdoc(mod)]
                + [
                    [name, val]
                    for name, val in mod.__dict__.items()
                    if callable(val) and modname + "." + name in live_actions
                ]
            )
        return all_action_sets

    def func_to_sexy_box(self, fname, func, ignore_args=[]):
        doc = getdoc(func)
        line = (
            "\\apispec{"
            + fname
            + "}{"
            + f"{self.format_params(signature(func), ignore_args=ignore_args)}"
            + "}\n"
        )
        parsed_doc = parse(doc)
        doc = parsed_doc.long_description
        if doc is None:
            doc = "No documentation yet."
        doc = doc.replace("_", " ")
        if len(parsed_doc.params):
            # doc += "\\vspace{3mm}\\par\n\\textbf{Parameters}\n\\par"
            doc += "\\vspace{4mm}\\par\n"
            args_doc = "\\argspec{Parameters}{"
            for i in parsed_doc.params:
                args_doc += (
                    f"\n\\texttt{{{i.arg_name}}} -"
                    f"- {i.description}\\vspace{{1.5mm}}\\par\n"
                )
            args_doc += "}"
            args_doc = args_doc.replace("_", "\\_")
            doc += args_doc
        if parsed_doc.returns:
            # doc += "\\vspace{3mm}\\par\n\\textbf{Parameters}\n\\par"
            doc += "\\vspace{4mm}\\par\n"
            args_doc = "\\argspec{Returns}{" + parsed_doc.returns.description + "}"
            args_doc = args_doc.replace("_", "\\_")
            doc += args_doc
        line += "{" + doc + "}\n"

        return line

    def bookgen_std_library(self):
        out = []
        for i in self.get_global_actions():
            lib = i[0]
            moddoc = parse(i[1]).long_description
            if moddoc is None:
                moddoc = "No documentation yet."
            if lib == "jaseci":
                continue
            out += ["\\subsection{" + lib + "}\n\\par\n" + moddoc + "\n"]
            i = i[2:]
            for j in i:
                out.append(
                    self.func_to_sexy_box(
                        ".".join([lib, j[0].replace("_", "\\_")]),
                        j[1],
                        ignore_args=["meta"],
                    )
                )
        return "".join(out)

    def std_library_table(self):
        out = []
        for i in self.get_global_actions():
            lib = i[0]
            if lib == "jaseci":
                continue
            out += ["\\subsection{" + lib + "}\n", self.get_stdlib_pre_table()]

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

    def bookgen_api_spec(self):
        ret = ""
        build_class_dict(jaseci)
        for i in obj_class_cache.keys():
            if not i.endswith("_api"):
                continue
            ret += f"\\subsection{{APIs for {i[:-4]}}}\n\n"
            doc = getdoc(obj_class_cache[i]).replace("\n\n", "\n\\par\n")
            doc = parse(doc).long_description
            doc = (
                doc.replace("_", "\\_") if doc is not None else "No documentation yet."
            )
            ret += f"{doc}\n\n"
            ret += self.api_call_spec(obj_class_cache[i])
        # return ret

    def api_call_spec(self, cls):
        ret = ""
        for i, v in cls.__dict__.items():
            # access = 'master'
            found = False
            auth_level = ""
            for j in Sm.all_apis(None, True):
                if i == j["fname"]:
                    found = True
                    auth_level = (
                        "public"
                        if j in Sm._public_api
                        else "user"
                        if j in Sm._private_api
                        else "admin"
                        if j in Sm._admin_api
                        else "cli_only"
                    )
                    break
            if not found:
                continue
            name = i.replace("_", " ")
            api = i.replace("_", "\\_")
            ret += (
                f"\\subsubsection{{\\lstinline"
                f"[basicstyle=\\Large\\ttfamily]${name}$}}\n\n"
            )
            authstr = "(cli only)"
            if auth_level != "cli_only":
                authstr = f"| api: {api} | auth: {auth_level}"
            ret += self.func_to_sexy_box(f"cli: {name} {authstr}", v)
        print(ret)
        return ret


# modified book class


class modifiedBook:
    def format_params(self, sig, ignore_args=[]):
        ret = ""
        for i in sig.parameters:
            if i == "self" or i in ignore_args:
                continue
            if len(ret):
                ret += ", "
            ret += i + ": " + sig.parameters[i].annotation.__name__
            default = sig.parameters[i].default
            if default == sig.parameters[i].empty:
                ret += " (*req)"
            else:
                # if isinstance(default, str):
                #     default = default.encode("unicode_escape").lstrip("b")
                default = (
                    str(default)
                    .replace("_", "\\_")
                    .replace("{", "\\{")
                    .replace("}", "\\}")
                    .replace("\n", "\\\\n")
                )
                ret += f" ({default})"
        return ret if len(ret) else "n/a"

    def bookgen_api_cheatsheet(self, root, out=None, str=""):
        if out is None:
            out = []
        line = "<tr> \n"
        if "leaf" in root.keys():
            line = "<tr> \n <td>" + str.strip()
            if root["leaf"][5]:  # cli_only
                line += " (cli only)"
            line += "</td>"
            line += "<td> \n <ul>"
            arguments = self.format_params(root["leaf"][1])
            arguments = arguments.split(",")
            for argument in arguments:
                line += "<li>" + f"{argument}" + "</li>\n"
            line += "</ul> \n </td> \n </tr>"
            out.append(line)
            return
        for i in root.keys():
            self.bookgen_api_cheatsheet(root[i], out, str + f"{i} ")
        all_info = "".join(out)
        return (
            "<table id='cheatsheet'>  <tr> <th>Interface</th> <th>Parameters</th> </tr>"
            + all_info
            + "</table>"
        )

    def get_stdlib_pre_table(self):
        clip = (
            "\\rowcolors{1}{light-cyan}{light-gray}\\begin{longtable}"
            "{|p{4cm} | p{6cm}|}\\toprule\\rowcolor{white}\\textbf"
            "{Action}&\\textbf{Args}\\\\\\midrule"
        )
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

    def get_global_actions(self):
        import jaseci.extens.act_lib as stdact
        import pkgutil
        from importlib.machinery import SourceFileLoader
        from jaseci.jsorc.live_actions import live_actions

        all_action_sets = []
        for importer, modname, ispkg in pkgutil.iter_modules(stdact.__path__):
            if not exists(stdact.__path__[0] + "/" + modname + ".py"):
                continue
            mod = SourceFileLoader(
                modname, stdact.__path__[0] + "/" + modname + ".py"
            ).load_module()
            all_action_sets.append(
                [modname]
                + [getdoc(mod)]
                + [
                    [name, val]
                    for name, val in mod.__dict__.items()
                    if callable(val) and modname + "." + name in live_actions
                ]
            )
        return all_action_sets

    def func_to_sexy_box(self, fname, func, ignore_args=[]):
        doc = getdoc(func)
        line = (
            "\ <div class='actionName'> "
            + fname
            + " </div> \n <div class ='actionsArgs'> "
            + f"{self.format_params(signature(func), ignore_args=ignore_args)}"
            + "</div>\n"
        )
        line = line.replace("\\", "")
        parsed_doc = parse(doc)
        doc = parsed_doc.long_description
        if doc is None:
            doc = "No documentation yet."
        doc = doc.replace("_", " ")
        if len(parsed_doc.params):
            # doc += "\\vspace{3mm}\\par\n\\textbf{Parameters}\n\\par"
            doc += "<div class='heading'>Params</div> \n <div class='params'> Params"
            # args_doc = "\\argspec{Parameters}{"
            args_doc = " "
            for i in parsed_doc.params:
                args_doc += f"\n{i.arg_name} -" f"- {i.description} <br> \n"
            args_doc += "</div>"

            doc += args_doc
        if parsed_doc.returns:
            # doc += "\\vspace{3mm}\\par\n\\textbf{Parameters}\n\\par"
            doc += "<div class='heading'>Returns</div> \n<div class='return'>"
            args_doc = "Returns - " + parsed_doc.returns.description
            args_doc = args_doc.replace("_", "\\_")
            doc += args_doc
        line += (
            " <div class ='mainbody'> <div class ='actionsDescription'>"
            + doc
            + "</div> </div> \n \n"
        )
        return line

    def bookgen_std_library(self):
        out = []
        for i in self.get_global_actions():
            lib = i[0]
            moddoc = parse(i[1]).long_description
            if moddoc is None:
                moddoc = "No documentation yet."
            if lib == "jaseci":
                continue
            out += ["\n" + "# " + lib + "\n\n" + moddoc + "\n"]
            i = i[2:]
            for j in i:
                out.append(
                    self.func_to_sexy_box(
                        ".".join([lib, j[0]]),
                        j[1],
                        ignore_args=["meta"],
                    )
                )

        return "".join(out)

    def std_library_table(self):
        out = []
        for i in self.get_global_actions():
            lib = i[0]
            if lib == "jaseci":
                continue
            out += ["\\subsection{" + lib + "}\n", self.get_stdlib_pre_table()]

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

    def bookgen_api_spec(self):
        ret = ""
        build_class_dict(jaseci)
        for i in obj_class_cache.keys():
            if not i.endswith("_api"):
                continue
            ret += f" # APIs for {i[:-4]}\n\n"
            doc = getdoc(obj_class_cache[i]).replace("\n\n", "\n\n")
            doc = parse(doc).long_description
            doc = (
                doc.replace("_", "\\_") if doc is not None else "No documentation yet."
            )
            ret += f"{doc}\n\n"
            ret += self.api_call_spec(obj_class_cache[i])
        return ret

    def api_call_spec(self, cls):
        ret = ""
        for i, v in cls.__dict__.items():
            # access = 'master'
            found = False
            auth_level = ""
            for j in Sm.all_apis(None, True):
                if i == j["fname"]:
                    found = True
                    auth_level = (
                        "public"
                        if j in Sm._public_api
                        else "user"
                        if j in Sm._private_api
                        else "admin"
                        if j in Sm._admin_api
                        else "cli_only"
                    )
                    break
            if not found:
                continue
            name = i.replace("_", " ")
            api = i.replace("_", "\\_")
            ret += f"<div class='actionHeading'>{name}</div>\n\n"
            authstr = "(cli only)"
            if auth_level != "cli_only":
                authstr = f"| api: {api} | auth: {auth_level}"
            ret += self.func_to_sexy_box(f"cli: {name} {authstr}", v)
        return ret
