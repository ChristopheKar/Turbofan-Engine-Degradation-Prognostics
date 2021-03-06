import numpy as np
from torch import nn

class GRU(nn.Module):
    def __init__(
        self, device,
        input_dim, hidden_dim, output_dim,
        n_layers, drop_prob=0.2):

        super().__init__()
        self.device = device
        self.hidden_dim = hidden_dim
        self.n_layers = n_layers

        self.gru = nn.GRU(
            input_dim,
            hidden_dim,
            n_layers,
            batch_first=True,
            dropout=drop_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self.relu = nn.ReLU()


    def forward(self, x, h):
        out, h = self.gru(x, h)
        out = self.fc(self.relu(out[:,-1]))
        return out, h


    def init_hidden(self, batch_size):
        weight = next(self.parameters()).data
        hidden = weight.new(
            self.n_layers,
            batch_size,
            self.hidden_dim).zero_().to(self.device)
        return hidden
