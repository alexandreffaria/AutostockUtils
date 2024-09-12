import torch
from transformers import AutoModelForCausalLM, AutoProcessor
from PIL import Image
import base64
from io import BytesIO

class ImageDescriber:
    def __init__(self, model_id="microsoft/Phi-3.5-vision-instruct", device="cuda:0", num_crops=4):
        self.model_id = model_id
        
        # Set _attn_implementation if flash_attention_2 is available
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            device_map="cuda",
            trust_remote_code=True,
            torch_dtype="auto",
            _attn_implementation="eager"
        )

        # For best performance, use num_crops=4 for multi-frame, num_crops=16 for single-frame
        self.processor = AutoProcessor.from_pretrained(
            model_id,
            trust_remote_code=True,
            num_crops=num_crops
        )
        
        self.device = device
    
    def load_image_as_base64(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    
    def describe_image(self, image_path):
        base64_image = self.load_image_as_base64(image_path)
        image_bytes = base64.b64decode(base64_image)
        image = Image.open(BytesIO(image_bytes))
        
        placeholder = "<|image_1|>\n"

        messages = [
            {
                "role": "user",
                "content": placeholder + "Describe this image as if you were talking to a blind person in an art gallery.",
            }
        ]

        prompt = self.processor.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.processor(prompt, images=[image], return_tensors="pt").to(self.device)

        generation_args = {
            "max_new_tokens": 1000,
            "temperature": 0.0,
            "do_sample": False,
        }

        generate_ids = self.model.generate(
            **inputs,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            **generation_args
        )

        # Remove input tokens
        generate_ids = generate_ids[:, inputs['input_ids'].shape[1]:]
        response = self.processor.batch_decode(
            generate_ids,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False
        )[0]

        return response

# Example usage:
if __name__ == "__main__":
    image_describer = ImageDescriber()
    description = image_describer.describe_image("imageDescription/2.png")
    print(description)
