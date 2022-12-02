from torch.utils.data import DataLoader
from .entitydataset import get_id_to_label


def eval_model(model, tokenizer, test_dataset, train_config):
    dataloader = DataLoader(test_dataset, batch_size=train_config["eval_batch_size"])
    resp_data = []
    for batch in dataloader:
        model.eval()
        scores = model.predict_step(batch, None)
        resp_data.append(
            get_id_to_label(batch=batch, scores=scores, tokenizer=tokenizer)
        )
    return resp_data
