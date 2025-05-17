import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from abc import ABC, abstractmethod


class RetellerStrategy(ABC):

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @abstractmethod
    def summarize(self, text: str, max_length: int, num_beams: int):
        pass