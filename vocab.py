# vocab.py

from tokenizer import tokenize

class Vocab:
    def __init__(self):
        self.word2idx = {}
        self.idx2word = {}
        self.size = 0

        # special tokens
        self.add_word("<PAD>")
        self.add_word("<SOS>")
        self.add_word("<EOS>")
        self.add_word("<UNK>")

    def add_word(self, word):
        if word not in self.word2idx:
            self.word2idx[word] = self.size
            self.idx2word[self.size] = word
            self.size += 1

    def build(self, sentences):
        for sentence in sentences:
            for token in tokenize(sentence):
                self.add_word(token)

    def encode(self, sentence):
        tokens = tokenize(sentence)

        return [self.word2idx["<SOS>"]] + \
               [self.word2idx.get(t, self.word2idx["<UNK>"]) for t in tokens] + \
               [self.word2idx["<EOS>"]]

    def decode(self, indices):
        return [self.idx2word.get(i, "<UNK>") for i in indices]