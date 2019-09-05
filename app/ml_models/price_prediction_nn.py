import torch


class PricePredictionFeedForward(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, hidden_num, **kwargs):
        torch.nn.Module.__init__(self)
        self.fc = torch.nn.Linear(input_dim, hidden_dim)
        self.activation = torch.nn.ReLU()
        self.hidden = torch.nn.ModuleList()
        for _ in range(hidden_num - 1):
            self.hidden.append(torch.nn.Linear(hidden_dim, hidden_dim))
            self.hidden.append(self.activation)
        self.out_layer = torch.nn.Linear(hidden_dim, 1)

    def forward(self, X):
        out = self.fc(X)
        out = self.activation(out)
        for layer in self.hidden:
            out = layer(out)
        out = self.out_layer(out)
        return out


def train_nn(X, y, device, nn_params):
    learning_rate = nn_params.pop("learning_rate", 0.1)
    epochs = nn_params.pop("epochs", 100)

    X = torch.Tensor(X).to(device)
    y = torch.Tensor(y).to(device)
    model = PricePredictionFeedForward(**nn_params).to(device)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    model.eval()
    model.train()
    for epoch in range(epochs):
        optimizer.zero_grad()
        outputs = model(X)
        loss = criterion(outputs.squeeze(), y)
        loss.backward()
        optimizer.step()
    model.eval()
    return model


def load_nn_model(path, device, nn_params):
    nn_params.pop("learning_rate", None)
    nn_params.pop("epochs", None)
    model = PricePredictionFeedForward(**nn_params).to(device)
    model.load_state_dict(torch.load(path))
    return model
