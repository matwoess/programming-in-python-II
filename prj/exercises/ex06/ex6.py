import torch
from torch import Tensor
from typing import Tuple


def ex6(logits: Tensor, activation_function, threshold: Tensor, targets: Tensor) \
        -> Tuple[float, float, float, float, float, float]:
    # error handling
    if not torch.is_floating_point(logits):
        raise TypeError(f'logits must be of type torch.Tensor with dtype=float32, but is {type(logits)}')
    if not isinstance(threshold, Tensor):
        raise TypeError(f'threshold must be of type torch.Tensor, but is {type(threshold)}')
    if not isinstance(targets, Tensor) or targets.dtype != torch.bool:
        raise TypeError(f'targets must be of type torch.Tensor with dtype=bool, but is {type(targets)}')
    if len(logits.shape) != 1 or len(targets.shape) != 1:
        raise ValueError(f'logits tensor and targets tensor must be of shape (n_samples,)')
    if len(logits) != len(targets):
        raise ValueError(f'logits tensor and targets tensor must have same length')
    if len([v for v in targets if v]) == 0 or len([v for v in targets if not v]) == 0:
        raise ValueError(f'targets tensor must contain at least one positive and one negative value')
    # calculations
    n_samples = len(targets)
    output = activation_function(logits)
    prediction_mask = [b for b in output >= threshold]
    targets_mask = [b for b in targets >= threshold]
    tp = sum([1 for p, t in zip(prediction_mask, targets_mask) if t and p])
    tn = sum([1 for p, t in zip(prediction_mask, targets_mask) if not t and not p])
    fp = sum([1 for p, t in zip(prediction_mask, targets_mask) if not t and p])
    fn = sum([1 for p, t in zip(prediction_mask, targets_mask) if t and not p])
    assert tp + tn + fp + fn == n_samples
    P = tp + fn
    N = tn + fp
    tpr = 1.0 if P == 0 else tp / P
    tnr = 1.0 - tpr if N == 0 else tn / N  # not sure about that
    fpr = 1 - tnr
    fnr = 1 - tpr
    acc = (tp + tn) / n_samples
    bacc = (tpr + tnr) / 2
    return tpr, tnr, fpr, fnr, acc, bacc


if __name__ == "__main__":
    logits_tensor = torch.tensor([-10, 10, 15, 50, 10, 1, -1, 0], dtype=torch.float32)
    targets_tensor = torch.tensor([0, 1, 1, 0, 1, 0, 1, 1], dtype=torch.bool)
    func = torch.sigmoid
    thresh = torch.tensor(0.5, dtype=torch.float32)
    res = ex6(logits_tensor, func, thresh, targets_tensor)
    print(f'true positive rate = {res[0]}')
    print(f'true negative rate = {res[1]}')
    print(f'false positive rate = {res[2]}')
    print(f'false negative rate = {res[3]}')
    print(f'accuracy = {res[4]}')
    print(f'balanced accuracy = {res[5]}')
