import torch
from dataset_loader import build_dataset
from model_transformer import TransformerModel
from tokenizer import tokenize
from infer_transformer import predict, format_output


# Load dataset
inputs, outputs, in_vocab, out_vocab = build_dataset("dataset.txt")

# Load model
model = TransformerModel(in_vocab.size, out_vocab.size)
model.load_state_dict(torch.load("transformer.pth"))
model.eval()


# Decode ground truth
def decode_output(tensor):
    tokens = [
        out_vocab.idx2word[i.item()]
        for i in tensor
        if i.item() not in [0, 1, 2]
    ]
    return " ".join(tokens)


# Evaluation
total = len(inputs)
correct = 0
wrong_samples = []

for i in range(total):

    # Get input sentence
    input_tokens = [
        in_vocab.idx2word[idx.item()]
        for idx in inputs[i]
        if idx.item() not in [0, 1, 2]
    ]
    sentence = " ".join(input_tokens)

    # Ground truth
    true_output = decode_output(outputs[i])
    true_output = format_output(true_output)

    # Prediction
    pred_output = predict(sentence)
    pred_output = format_output(pred_output)

    # Compare
    if pred_output == true_output:
        correct += 1
    else:
        wrong_samples.append((sentence, true_output, pred_output))


# Accuracy
accuracy = (correct / total) * 100

print("\n==========================")
print(f"Total Samples: {total}")
print(f"Correct: {correct}")
print(f"Accuracy: {accuracy:.2f}%")
print("==========================\n")


# Show some wrong cases
print("Sample Errors:\n")

for i in range(min(10, len(wrong_samples))):
    s, t, p = wrong_samples[i]
    print(f"Input: {s}")
    print(f"Expected: {t}")
    print(f"Predicted: {p}")
    print("-" * 40)