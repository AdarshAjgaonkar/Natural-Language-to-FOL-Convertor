import torch
import torch.nn as nn
import torch.optim as optim

from dataset_loader import build_dataset
from model_transformer import TransformerModel

# ---------------- DEVICE ----------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ---------------- LOAD DATA ----------------
inputs, outputs, in_vocab, out_vocab = build_dataset("dataset.txt")

inputs = inputs.to(device)
outputs = outputs.to(device)

# ---------------- MODEL ----------------
model = TransformerModel(in_vocab.size, out_vocab.size).to(device)

criterion = nn.CrossEntropyLoss(ignore_index=0)
optimizer = optim.Adam(model.parameters(), lr=0.0003)

EPOCHS = 200

# ---------------- TRAIN ----------------
for epoch in range(EPOCHS):

    model.train()
    optimizer.zero_grad()

    # Teacher forcing
    output = model(inputs, outputs[:, :-1])

    output = output.reshape(-1, out_vocab.size)
    target = outputs[:, 1:].reshape(-1)

    loss = criterion(output, target)

    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)  # stability
    optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# ---------------- SAVE (FIXED) ----------------
torch.save({
    "model": model.state_dict(),
    "in_vocab": in_vocab,
    "out_vocab": out_vocab
}, "transformer.pth")

print("\nTraining complete. Model saved as transformer.pth")