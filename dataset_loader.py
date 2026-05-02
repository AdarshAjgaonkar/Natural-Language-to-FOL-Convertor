# dataset_loader.py

import torch
from vocab import Vocab

def build_dataset(file):
    inputs = []
    outputs = []

    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if "\t" in line:
                inp, out = line.strip().split("\t")
                inputs.append(inp)
                outputs.append(out)

    in_vocab = Vocab()
    out_vocab = Vocab()

    in_vocab.build(inputs)
    out_vocab.build(outputs)

    encoded_inputs = [in_vocab.encode(s) for s in inputs]
    encoded_outputs = [out_vocab.encode(s) for s in outputs]

    max_in = max(len(x) for x in encoded_inputs)
    max_out = max(len(x) for x in encoded_outputs)

    def pad(seq, max_len):
        return seq + [0] * (max_len - len(seq))

    inputs_tensor = torch.tensor([pad(x, max_in) for x in encoded_inputs])
    outputs_tensor = torch.tensor([pad(x, max_out) for x in encoded_outputs])

    return inputs_tensor, outputs_tensor, in_vocab, out_vocab