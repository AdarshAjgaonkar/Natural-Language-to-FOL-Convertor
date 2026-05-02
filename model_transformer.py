import torch
import torch.nn as nn

class TransformerModel(nn.Module):

    def __init__(self, input_dim, output_dim, embed_size=128, n_heads=4, n_layers=2):
        super().__init__()

        self.embedding_in = nn.Embedding(input_dim, embed_size)
        self.embedding_out = nn.Embedding(output_dim, embed_size)

        self.transformer = nn.Transformer(
            d_model=embed_size,
            nhead=n_heads,
            num_encoder_layers=n_layers,
            num_decoder_layers=n_layers,
            batch_first=True
        )

        self.fc = nn.Linear(embed_size, output_dim)

    def forward(self, src, tgt):

        src_emb = self.embedding_in(src)
        tgt_emb = self.embedding_out(tgt)

        # 🔥 CRITICAL: causal mask (prevents cheating + repetition)
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(
            tgt_emb.size(1)
        ).to(tgt.device)

        out = self.transformer(src_emb, tgt_emb, tgt_mask=tgt_mask)

        return self.fc(out)