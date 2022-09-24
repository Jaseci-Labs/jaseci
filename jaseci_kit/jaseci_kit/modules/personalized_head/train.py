import argparse
import torch
import numpy as np
import os
from pathlib import Path

import utils.loss as loss_module
import utils.metric as metric_module
import utils.model as model_module
import utils.dataloader as dataloader_module

from utils.trainer import Trainer
from utils import prepare_device, read_yaml
from utils.logger import setup_logging


# fix random seeds for reproducibility
SEED = 123
torch.manual_seed(SEED)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
np.random.seed(SEED)


def main(args):
    if args.device is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.device

    # Loading Configuration
    if args.resume is not None:
        resume = Path(args.resume)
        cfg_fname = resume.parent / 'config.yaml'
    else:
        msg_no_cfg = "Configuration file need to be specified. Add '-c config.yaml', for example."
        assert args.config is not None, msg_no_cfg
        resume = None
        cfg_fname = Path(args.config)

    config = read_yaml(cfg_fname)
    if args.config and resume:
        # update new config for fine-tuning
        config.update(read_yaml(args.config))

    #Setup Logger
    log_config = config['Logger']
    setup_logging(log_config)

    # Build model Architecture
    model_config = config['Model']
    model = getattr(model_module, model_config['type'])(**model_config['args'])

    trainer_config = config['Trainer']

    # Setup Dataloader
    dataloader = getattr(dataloader_module, trainer_config['dataloader']['type'])(
        **trainer_config['dataloader']['args'])
    valid_dataloader = dataloader.split_validation()

    # for multi-GPU training
    device, device_ids = prepare_device(trainer_config['n_gpu'])
    model = model.to(device)
    if len(device_ids) > 1:
        model = torch.nn.DataParallel(model, device_ids=device_ids)

    # get function handles of loss and metrics
    criterion = getattr(loss_module, trainer_config['loss'])
    metrics = [getattr(metric_module, metric)
               for metric in trainer_config['metrics']]

    # build optimizer, learning rate scheduler. delete every lines containing lr_scheduler for disabling scheduler
    trainable_params = filter(lambda p: p.requires_grad, model.parameters())
    optimizer = getattr(torch.optim, trainer_config['optimizer']['type'])(
        trainable_params, **trainer_config['optimizer']['args'])
    lr_scheduler = getattr(torch.optim.lr_scheduler, trainer_config['lr_scheduler']['type'])(
        optimizer, **trainer_config['lr_scheduler']['args'])

    trainer = Trainer(model, criterion, metrics, optimizer,
                      config=trainer_config,
                      device=device,
                      data_loader=dataloader,
                      valid_data_loader=valid_dataloader,
                      lr_scheduler=lr_scheduler)

    trainer.train()


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='PyTorch Template')
    args.add_argument('-c', '--config', default=None, type=str,
                      help='config file path (default: None)')
    args.add_argument('-r', '--resume', default=None, type=str,
                      help='path to latest checkpoint (default: None)')
    args.add_argument('-d', '--device', default=None, type=str,
                      help='indices of GPUs to enable (default: all)')
    args = args.parse_args()

    main(args)
