import importlib
from datetime import datetime
import logging
import logging.config
from pathlib import Path
import os

log_levels = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}


class TensorboardWriter:
    def __init__(self, log_dir, logger, enabled):
        self.writer = None
        self.selected_module = ""

        if enabled:
            log_dir = str(log_dir)

            # Retrieve vizualization writer.
            succeeded = False
            for module in ["torch.utils.tensorboard", "tensorboardX"]:
                try:
                    self.writer = importlib.import_module(module).SummaryWriter(log_dir)
                    succeeded = True
                    break
                except ImportError:
                    succeeded = False
                self.selected_module = module

            if not succeeded:
                message = (
                    "Warning: visualization (Tensorboard) is configured to use, but currently not installed on "
                    "this machine. Please install TensorboardX with 'pip install tensorboardx', upgrade PyTorch to "
                    "version >= 1.1 to use 'torch.utils.tensorboard' or turn off the option in the 'config.yaml' file."
                )
                logger.warning(message)

        self.step = 0
        self.mode = ""

        self.tb_writer_ftns = {
            "add_scalar",
            "add_scalars",
            "add_image",
            "add_images",
            "add_audio",
            "add_text",
            "add_histogram",
            "add_pr_curve",
            "add_embedding",
        }
        self.tag_mode_exceptions = {"add_histogram", "add_embedding"}
        self.timer = datetime.now()

    def set_step(self, step, mode="train"):
        self.mode = mode
        self.step = step
        if step == 0:
            self.timer = datetime.now()
        else:
            duration = datetime.now() - self.timer
            self.add_scalar("steps_per_sec", 1 / duration.total_seconds())
            self.timer = datetime.now()

    def __getattr__(self, name):
        """
        If visualization is configured to use:
            return add_data() methods of tensorboard with additional information (step, tag) added.
        Otherwise:
            return a blank function handle that does nothing
        """
        if name in self.tb_writer_ftns:
            add_data = getattr(self.writer, name, None)

            def wrapper(tag, data, *args, **kwargs):
                if add_data is not None:
                    # add mode(train/valid) tag
                    if name not in self.tag_mode_exceptions:
                        tag = "{}/{}".format(tag, self.mode)
                    add_data(tag, data, self.step, *args, **kwargs)

            return wrapper
        else:
            # default action for returning methods defined in this class, set_step() for instance.
            try:
                attr = object.__getattr__(name)
            except AttributeError:
                raise AttributeError(
                    "type object '{}' has no attribute '{}'".format(
                        self.selected_module, name
                    )
                )
            return attr


# FIXME: dictConfig is not loading
def setup_logging(log_config=None, default_level=logging.INFO):
    """
    Setup logging configuration
    """
    save_dir = log_config["log_dir"]
    os.makedirs(save_dir, exist_ok=True)
    if log_config:
        for _, handler in log_config["handlers"].items():
            if "filename" in handler:
                handler["filename"] = str(Path(save_dir) / handler["filename"])
        logging.config.dictConfig(log_config)
    else:
        print(
            "Warning: logging configuration file is not found in {}.".format(log_config)
        )
        logging.basicConfig(level=default_level)


def get_logger(name, verbosity=2):
    msg_verbosity = "verbosity option {} is invalid. Valid options are {}.".format(
        verbosity, log_levels.keys()
    )
    assert verbosity in log_levels, msg_verbosity
    logger = logging.getLogger(name)
    logger.setLevel(log_levels[verbosity])
    return logger
