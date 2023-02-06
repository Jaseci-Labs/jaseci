import os
import pathlib
import shutil
import tempfile

import git
from jaseci.actions.live_actions import load_module_actions
from jaseci.svc import MetaService
from jaseci.utils.utils import logger

curr_path = pathlib.Path().resolve()


class JacExecutable:
    def __init__(self, run_svcs=False):
        self.meta = MetaService(run_svcs=run_svcs)
        self.smast = self.meta.build_super_master()
        self.mast = self.meta.build_master(h=self.smast._h)

    def call(self, mast, pl):
        ret = mast.general_interface_to_api(api_name=pl[0], params=pl[1])
        return ret

    def load_jac(self, fn):
        with open(fn) as f:
            return f.read()

    def train(self, jac_file, train_file):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac(jac_file)}],
        )
        return self.call(
            self.mast,
            ["walker_run", {"name": "train", "ctx": {"train_file": train_file}}],
        )

    def run_main_jac(self, jac_file):
        self.call(
            self.mast,
            ["sentinel_register", {"code": self.load_jac(jac_file)}],
        )
        return self.call(self.mast, ["walker_run", {"name": "init"}])


def update_file(infile):
    data = open(infile, "r")
    find = 'import {*} with "./graph.jac";'
    replace = 'import {*} with "sample_bot/graph.jac";'

    data_str = ""
    find_str = ""
    replace_str = ""

    for line in data:  # concatenate it into one long string
        data_str += line

    for line in find:  # concatenate it into one long string
        find_str += line

    for line in replace:
        replace_str += line

    return data_str.replace(find, replace)  # return updated jac code


def chat_setup():
    try:
        # Create temporary dir
        base_path = tempfile.mkdtemp()
        # Clone into temporary dir
        git.Repo.clone_from(
            "https://github.com/Jaseci-Labs/jaseci.git",
            base_path,
            branch="main",
            depth=1,
        )
        # Copy desired file from temporary dir
        # shutil.move(os.path.join(base_path, 'test.sh'), '.')
        # Remove temporary dir
        base_dir = curr_path / "sample_bot"
        data_dir = base_dir / "data_dir"

        isExist = os.path.exists(data_dir)
        if not isExist:
            os.makedirs(data_dir)
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/code/clf_train_2.json"),
            data_dir / "bi_train.json",
        )
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/code/ner_train.json"),
            data_dir / "ner_train.json",
        )

        model_dir = base_dir / "model_dir"
        isExist = os.path.exists(model_dir)
        if not isExist:
            os.makedirs(model_dir)
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/code/tfm_ner.jac"),
            model_dir / "tfm_ner.jac",
        )
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/code/bi_enc.jac"),
            model_dir / "bi_enc.jac",
        )
        updated_jac = update_file(
            os.path.join(base_path, "examples/CanoniCAI/reference/tesla_ai.jac")
        )
        # update jac code import
        with open((base_dir / "jac_talk.jac"), "w") as fp:
            fp.write(updated_jac)
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/reference/faq.jac"),
            base_dir / "faq.jac",
        )
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/reference/graph.jac"),
            base_dir / "graph.jac",
        )
        shutil.copy2(
            os.path.join(base_path, "examples/CanoniCAI/reference/dialogue.jac"),
            base_dir / "dialogue.jac",
        )
        shutil.rmtree(base_path)
    except Exception as e:
        shutil.rmtree(base_path)
        logger.error(f"Failed to copy files to current path: {e}")


def load_model(model_name):
    try:
        return load_module_actions(f"jac_nlp.{model_name}")
    except Exception as e:
        logger.error(f"Failed to load model {model_name}: {e}")


def train_model():
    try:
        if load_model("tfm_ner"):
            train_file = curr_path / "sample_bot/data_dir/ner_train.json"
            jac_file = curr_path / "sample_bot/model_dir/tfm_ner.jac"
            run_fl = JacExecutable()
            run_fl.train(jac_file, train_file)
        else:
            logger.error("unable to load NER model")
            return
        if load_model("bi_enc"):
            train_file = curr_path / "sample_bot/data_dir/bi_train.json"
            jac_file = curr_path / "sample_bot/model_dir/bi_enc.jac"
            run_fl = JacExecutable()
            run_fl.train(jac_file, train_file)
        else:
            logger.error("unable to load intent detection model")
            return
        if load_model("use_enc"):
            logger.info("model training and loading completed")
        else:
            logger.error("unable to load encoding model")
            return
    except Exception as e:
        logger.error(f"Failed to load model: {e}")


def run_jactalk_shell():
    jac_file = curr_path / "sample_bot/jac_talk.jac"
    run_fl = JacExecutable()
    run_fl.run_main_jac(jac_file)
