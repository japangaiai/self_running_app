from django.db import models
import torch
import torch.nn as nn
import torch.optim as optim
from torch.nn import functional as F
from torchmetrics.functional import accuracy
import pytorch_lightning as pl
import torchvision


class Test(models.Model):
    pass


class ModelFile(models.Model):
    image = models.ImageField(upload_to='documents/')


class Net(pl.LightningModule):

    def __init__(self):
        super().__init__()

        self.feature = torchvision.models.resnet18(pretrained=True)
        self.fc = nn.Linear(1000, 4)

    def forward(self, x):
        h = self.feature(x)
        h = self.fc(h)
        return h

    def training_step(self, batch, batch_idx):
        x, t = batch
        y = self(x)
        loss = F.cross_entropy(y, t)
        self.log('train_loss', loss, on_step=False, on_epoch=True)
        self.log('train_acc', accuracy(y.softmax(dim=-1), t),
                 on_step=False, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
        x, t = batch
        y = self(x)
        loss = F.cross_entropy(y, t)
        self.log('val_loss', loss, on_step=False, on_epoch=True)
        self.log('val_acc', accuracy(y.softmax(dim=-1), t),
                 on_step=False, on_epoch=True)
        return loss

    def test_step(self, batch, batch_idx):
        x, t = batch
        y = self(x)
        loss = F.cross_entropy(y, t)
        self.log('test_loss', loss, on_step=False, on_epoch=True)
        self.log('test_acc', accuracy(y.softmax(dim=-1), t),
                 on_step=False, on_epoch=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.SGD(self.parameters(), lr=0.01)
        return optimizer
