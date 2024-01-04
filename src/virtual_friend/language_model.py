import tokenize
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


class LanguageModel():

    def __init__(self, cuda_device_id:int=1):
        self.pretrained_model_name = "line-corporation/japanese-large-lm-3.6b-instruction-sft"

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.pretrained_model_name,
            use_fast=False,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.pretrained_model_name,
            torch_dtype=torch.float16
        )

        self.generator = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=cuda_device_id,
        )

    def generate(self, prompt:str):
        output = self.generator(
            prompt,
            max_new_tokens=64,
            do_sample=True,
            temperature = 0.7,
            top_p = 0.9,
            top_k = 0,
            repetition_penalty = 1.1,
            num_beams = 1,
            pad_token_id = self.tokenizer.pad_token_id,
            num_return_sequences = 1,
        )
        print(output)
        return output[0]["generated_text"]

    def __call__(self, prompt:str):
        return self.generate(prompt)
