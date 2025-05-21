from ..reteller_strategy import RetellerStrategy


class RuT5Reteller(RetellerStrategy):

    def __init__(self):
        super().__init__(model_name='/app/ruT5-base-summarizer')

    def summarize(self,
                  text: str,
                  max_length: int,
                  num_beams: int = 5,
                  top_k: int = 50,
                  top_p: float = 0.9,
                  temperature: float = 0.7,
                  repetition_penalty: float = 10.0):
        inputs = self.tokenizer(
            f"перефразируй: {text}",
            return_tensors='pt',
            padding=True,
            truncation=True,
            max_length=max_length
        ).to(self.device)

        outputs = self.model.generate(
            **inputs,
            do_sample=True,
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_beams=10,
            early_stopping=True,
            repetition_penalty=5.0
        )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
