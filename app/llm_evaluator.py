from PIL import Image
from llava.model.builder import load_pretrained_model
from llava.mm_utils import get_model_name_from_path
import torch

def load_llava_model(model_path="liuhaotian/llava-v1.5-7b"):
    model_name = get_model_name_from_path(model_path)
    return load_pretrained_model(
        model_path=model_path,
        model_base=None,
        model_name=model_name,
        load_4bit=True,      
        device_map="auto",    
        torch_dtype=torch.float16
    )
class LLaVAChecker:
    def __init__(self):
        self.model_path = "liuhaotian/llava-v1.5-7b"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.load_model()
    
    def load_model(self):
        self.model_name = get_model_name_from_path(self.model_path)
        self.tokenizer, self.model, self.image_processor, self.context_len = load_pretrained_model(
            model_path=self.model_path,
            model_base=None,
            model_name=self.model_name,
            load_4bit=True,
            device_map="auto",
            torch_dtype=torch.float16
        )
    
    def generate_prompt(self, brand_data):
        return f"""
        You are a brand compliance assistant. The uploaded image is a marketing asset. Your role is to ensure that the image is following
        the right brand kit rules. 

        Here are the brand kit compliance rules:
        FONTS: font style used should be 
        - Primary: {brand_data['fonts'][0]}
        - Secondary: {brand_data['fonts'][1]}        
        COLORS:
        - Primary: the primiary colors used in the logo should be {brand_data['primary_colors']}
        - Allowed: the color palette used in the image should be {brand_data['color_palette']}
        SAFE ZONE: 
        - Minimum padding: {brand_data['safe_zone']}
        
        ASSESSMENT:
        There are 4 elements to be assessed for the overall grade in range [0, 4], 
        where each requirement being satisfied should contribute a single point to the overall grade. Check for:
        1. Font style compliance (primary/secondary usage)
        2. Color usage (dominant colors should match brand palette)
        3. Logo placement (should respect safe zone)
        4. Logo colors (primiary colors used in the logo)

        Return JSON format:
        {{
            "score": 0-4,
            "details": {{
                "font_compliance": {{"score": 0|1, "explanation": str}},
                "color_compliance": {{"score": 0|1, "explanation": str}},
                "logo_placement": {{"score": 0|1, "explanation": str}},
                "logo_colors_compliance": {{"score": 0|1, "explanation": str}}
            }},
            "overall_feedback": str
        }}
        """

    def check_compliance(self, image_path, brand_data):
        prompt = self.generate_prompt(brand_data)
        image = Image.open(image_path)
        
        from llava.eval.run_llava import eval_model
        args = type('Args', (), {
            "model_name": self.model_name,
            "query": prompt,
            "conv_mode": None,
            "image_file": image_path,
            "image": image,
            "temperature": 0,
            "top_p": None,
            "num_beams": 1,
            "max_new_tokens": 512
        })()
        
        result = eval_model(args, self.tokenizer, self.model, self.image_processor, self.context_len)
        return self.parse_response(result)

    def parse_response(self, response_text):
        import json
        try:
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            return json.loads(response_text[start_idx:end_idx])
        except:
            return {"error": "Failed to parse LLM response"}
