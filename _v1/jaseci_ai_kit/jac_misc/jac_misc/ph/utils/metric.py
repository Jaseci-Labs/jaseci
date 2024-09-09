import torch


def accuracy(output, target):
    with torch.no_grad():
        pred = torch.argmax(output, dim=1)
        assert pred.shape[0] == len(target)
        correct = 0
        correct += torch.sum(pred == target).item()
    return correct / len(target)


def top_k_acc(output, target, k=3):
    with torch.no_grad():
        pred = torch.topk(output, k, dim=1)[1]
        assert pred.shape[0] == len(target)
        correct = 0
        for i in range(k):
            correct += torch.sum(pred[:, i] == target).item()
    return correct / len(target)


# mean squared error
def mse(output, target):
    with torch.no_grad():
        batch_size = target.size(0)
        diff = torch.square(output - target) / batch_size
        diff = diff.sum()
    return diff


# mean absolute error
def mae(output, target):
    with torch.no_grad():
        batch_size = target.size(0)
        diff = torch.abs(output - target) / batch_size
        diff = diff.sum()
    return diff
