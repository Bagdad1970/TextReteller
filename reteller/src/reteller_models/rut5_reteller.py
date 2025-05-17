from ..reteller_strategy import RetellerStrategy


class RuT5Reteller(RetellerStrategy):

    def __init__(self):
        super().__init__(model_name='sarahai/ruT5-base-summarizer')

    def summarize(self, text: str, max_length: int, num_beams: int = 5):
        """prompt = f"summarize: {text}"
        input_ids = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=1000,
            truncation=True
        )["input_ids"].to(self.device)

        output_ids = self.model.generate(
            input_ids,
            max_length=150,
            min_length=50,
            num_beams=4,
            no_repeat_ngram_size=3,
            early_stopping=True
        )
        summary = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return summary"""

        return f'Заглушка к тексту \"{text}\"'

