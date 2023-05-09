import torch
import torch.nn as nn
import numpy as np
import torch.nn.functional as F
import matplotlib.pyplot as plt


class predictor(nn.Module):
    def __init__(self, hidden_size=64, num_layer=1):
        super().__init__()
        self.lstm = nn.LSTM(2, hidden_size, num_layer)
        self.cls = nn.Linear(hidden_size, 8)

    def forward(self, x, y=None):
        if self.training:
            L = x.size(0)
            label = x[..., 0].clone().detach().long().squeeze(1)
            x, (hn, cn) = self.lstm(x)
            x = self.cls(x[:-1]).squeeze(1)
            loss = F.cross_entropy(x, label[1:], reduction='mean')
            return loss
        else:
            # evaluate
            x, (hn, cn) = self.lstm(x)
            x0 = x[-1].unsqueeze(0)
            pred = []
            for i in range(y.size(0)):
                y0 = self.cls(x0)
                l0 = torch.argmax(y0)
                if i == 0:
                    first_pred = l0
                pred.append(y0)
                x1 = torch.tensor([l0, y[i, 0, 1]]).float().unsqueeze(0).unsqueeze(0)
                x0, (hn, cn) = self.lstm(x1, (hn, cn))
            pred = torch.cat(pred).squeeze(1)
            gt = y[..., 0].long().squeeze(1)
            p = torch.argmax(pred, dim=-1)
            acc = torch.where(p == gt, 1, 0).sum() / p.size(0)
            # print('first pred hit: %d' % 1 if first_pred == int(y[0, 0, 0]) else 0)
            first_pred_hit = 1 if first_pred == int(y[0, 0, 0]) else 0
            return F.cross_entropy(pred, gt), acc, first_pred_hit


if __name__ == '__main__':
    data = list(
        # [[4, 1], [4, 1], [4, 2], [4, 1], [4, 1], [4, 1], [4, 2], [4, 2], [4, 2], [4, 0], [4, 0], [4, 1], [4, 0], [4, 0],
        #  [5, 0], [4, 2], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 6], [4, 0], [4, 5], [4, 6],
        #  [4, 3], [4, 0], [4, 7], [4, 1], [4, 1], [4, 0], [4, 1], [7, 3], [4, 1], [7, 4], [4, 1], [4, 0], [7, 2], [4, 6],
        #  [4, 0], [4, 0], [4, 3], [4, 3], [4, 6], [4, 6], [4, 1], [4, 5], [4, 1], [4, 0], [4, 1], [4, 7], [4, 8], [4, 1],
        #  [4, 1], [4, 1], [4, 1], [4, 4], [4, 2], [7, 1], [4, 0], [4, 2], [4, 3], [4, 2], [4, 2], [4, 1], [7, 1], [4, 0],
        #  [4, 1], [4, 3], [4, 0], [7, 0], [4, 3], [4, 6], [4, 1], [4, 3], [4, 3], [4, 4], [4, 1], [4, 2], [4, 1], [4, 0],
        #  [4, 5], [4, 0], [4, 4], [4, 0], [4, 1], [4, 2], [4, 2], [4, 1], [4, 1], [4, 1], [4, 1], [4, 1], [4, 0], [4, 1],
        #  [4, 8], [4, 0], [4, 0], [4, 1], [4, 4], [4, 0], [7, 1], [4, 0], [4, 3], [4, 1], [4, 5], [4, 1], [4, 6], [4, 1],
        #  [4, 4], [4, 6], [4, 5], [4, 1], [4, 1], [4, 0], [4, 0], [4, 3], [4, 1], [4, 0], [4, 2], [4, 0], [4, 1], [4, 0],
        #  [4, 0], [4, 0], [4, 0], [4, 0], [4, 0], [4, 1], [4, 1], [4, 2], [4, 2], [4, 1], [4, 2], [4, 6], [4, 1], [4, 2],
        #  [4, 0], [4, 2], [4, 2], [4, 1], [4, 0], [4, 3], [4, 0], [4, 1], [4, 5], [4, 1], [4, 1], [4, 5], [4, 2], [4, 5],
        #  [4, 1], [4, 2], [4, 0], [4, 0], [4, 2], [4, 2], [4, 2], [4, 2], [4, 0], [4, 0], [4, 1], [4, 2], [4, 2], [4, 0],
        #  [4, 0], [4, 1], [4, 0], [4, 3], [4, 4], [4, 0], [4, 1], [4, 1], [4, 1], [4, 1], [4, 1], [4, 1], [4, 2],
        #  [4, 10], [4, 1], [7, 2], [4, 1], [4, 4], [4, 1], [4, 1], [4, 3], [5, 1], [4, 0], [4, 1], [4, 0], [4, 0]]
        [[2, 0], [2, 1], [2, 1], [2, 0], [2, 0], [3, 0], [2, 1], [2, 1], [2, 0], [2, 0], [2, 0], [2, 0], [2, 0], [2, 0],
         [2, 1], [2, 2], [2, 0], [2, 0], [2, 3], [2, 0], [2, 1], [2, 1], [2, 0], [2, 0], [2, 0], [2, 0], [2, 0], [2, 2],
         [2, 1], [2, 0], [2, 3], [2, 1], [2, 1], [2, 0], [2, 0], [2, 1], [2, 0], [2, 2], [2, 0], [2, 6], [2, 0], [2, 0],
         [2, 0], [2, 0], [2, 0], [2, 6], [2, 0], [0, 1], [2, 1], [2, 8], [2, 1], [2, 1], [2, 2], [2, 1], [2, 5], [2, 0],
         [7, 1], [4, 1], [4, 2], [4, 3], [4, 2], [4, 1], [4, 15], [4, 5], [4, 1], [4, 4], [4, 1], [4, 1], [4, 2],
         [4, 3], [4, 2], [7, 10], [4, 0], [4, 0], [4, 10], [4, 5], [7, 1], [4, 2], [4, 3], [4, 1], [4, 1], [4, 0],
         [4, 1], [4, 1], [4, 0]]
    )
    data = np.array(data, dtype=float)
    l = int(data.shape[0] * 0.8)
    print('length of train sequence is: %d' % l)
    train = torch.tensor(data[:l], dtype=torch.float32).unsqueeze(1)
    test = torch.tensor(data[l:], dtype=torch.float32).unsqueeze(1)

    model = predictor()
    num_epoch = 200
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 10, 0.9)
    losses = []
    eval_losses = []
    accs = []
    for i in range(num_epoch):
        lr = scheduler.get_last_lr()[0]
        model.train()
        optimizer.zero_grad()
        loss = model(train)
        loss.backward()
        optimizer.step()
        scheduler.step()

        model.eval()
        eval_loss, acc, fph = model(train, test)
        print('[epoch: %d] lr: %f, loss: %f, eval_loss: %f, acc: %f, fph: %d' % (i, lr, loss, eval_loss, acc, fph))
        losses.append(float(loss))
        eval_losses.append(float(eval_loss))
        accs.append(float(acc))

    plt.figure(figsize=(10, 10), dpi=100)
    plt.plot(np.arange(1, num_epoch + 1, 1), np.array(losses), color='r', label='Train Loss')
    plt.plot(np.arange(1, num_epoch + 1, 1), np.array(eval_losses), color='g', label='Eval Loss')
    plt.plot(np.arange(1, num_epoch + 1, 1), np.array(accs), color='b', label='Acc')
    plt.legend()
    plt.xlabel("epochs")
    plt.ylabel("numerical value")

    plt.show()

    print('best acc: %f' % np.max(accs))
