import argparse
import torch
import os
from pathlib import Path

from .utils import loss as loss_module
from .utils import metric as metric_module
from .utils import model as model_module
from .utils import dataloader as dataloader_module

from .utils.trainer import Trainer
from .utils import prepare_device, read_yaml
from .utils.logger import setup_logging


def train(args):
    if args["device"] is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.device

    # Loading Configuration
    if args["resume"] is not None:
        resume = Path(args["resume"])
    else:
        resume = None

    msg_no_cfg = (
        "Configuration file need to be specified. Add '-c config.yaml', for example."
    )
    assert args["config"] is not None, msg_no_cfg
    cfg_fname = Path(args["config"])

    config = read_yaml(cfg_fname)

    # Setup Logger
    log_config = config["Logger"]
    setup_logging(log_config)

    # Build model Architecture
    model_config = config["Model"]
    model = getattr(model_module, model_config["type"])(**model_config.get("args", {}))

    trainer_config = config["Trainer"]

    # Setup Dataloader
    dataloader = getattr(dataloader_module, trainer_config["dataloader"]["type"])(
        **trainer_config["dataloader"].get("args", {})
    )
    valid_dataloader = dataloader.split_validation()

    # for multi-GPU training
    device, device_ids = prepare_device(trainer_config["n_gpu"])
    model = model.to(device)
    if len(device_ids) > 1:
        model = torch.nn.DataParallel(model, device_ids=device_ids)

    # get function handles of loss and metrics
    if trainer_config["loss"] == "custom_loss":
        criterion = getattr(loss_module, "CustomLoss")(
            **trainer_config.get("loss_args", {})
        )
    elif trainer_config["loss"] == "vector_similarity_loss":
        criterion = getattr(loss_module, "VectorSimilarityLoss")(
            **trainer_config.get("loss_args", {})
        )
    else:
        criterion = getattr(loss_module, trainer_config["loss"])

    metrics = [getattr(metric_module, metric) for metric in trainer_config["metrics"]]

    # build optimizer, learning rate scheduler. delete every lines containing lr_scheduler for disabling scheduler
    trainable_params = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = getattr(torch.optim, trainer_config["optimizer"]["type"])(
        trainable_params, **trainer_config["optimizer"].get("args", {})
    )
    lr_scheduler = getattr(
        torch.optim.lr_scheduler, trainer_config["lr_scheduler"]["type"]
    )(optimizer, **trainer_config["lr_scheduler"].get("args", {}))

    trainer = Trainer(
        model,
        criterion,
        metrics,
        optimizer,
        config=trainer_config,
        device=device,
        data_loader=dataloader,
        valid_data_loader=valid_dataloader,
        lr_scheduler=lr_scheduler,
        resume=resume,
        uuid=args["uuid"],
    )

    trainer.train()
    return trainer.run_id


if __name__ == "__main__":
    args = argparse.ArgumentParser(description="PyTorch Template")
    args.add_argument(
        "-c",
        "--config",
        default=None,
        type=str,
        help="config file path (default: None)",
    )
    args.add_argument(
        "-r",
        "--resume",
        default=None,
        type=str,
        help="path to latest checkpoint (default: None)",
    )
    args.add_argument(
        "-d",
        "--device",
        default=None,
        type=str,
        help="indices of GPUs to enable (default: all)",
    )
    args.add_argument(
        "-u",
        "--uuid",
        default=None,
        type=str,
        help="uuid of the experiment (default: None)",
    )
    args = args.parse_args()
    # convert args to dict
    args = vars(args)
    train(args)
