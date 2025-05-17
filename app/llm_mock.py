from PIL import Image
import random
import json

class MockLLaVAChecker:
    def __init__(self):
        # Simulate model loading
        print("Initializing mock LLaVA checker...")
        
    def generate_mock_response(self, brand_data):
        font_score = random.choice([0, 1])
        color_score = random.choice([0, 1])
        logo_placement_score = random.choice([0, 1])
        logo_color_score = random.choice([0, 1])
        total_score = font_score + color_score + logo_placement_score + logo_color_score
        
        return {
            "score": total_score,
            "details": {
                "font_compliance": {
                    "score": font_score,
                    "explanation": "Uses brand font '{}'".format(brand_data['fonts'][0]) if font_score else "Incorrect font detected"
                },
                "color_compliance": {
                    "score": color_score,
                    "explanation": "Colors match brand palette" if color_score else "Color #FF0000 violates brand rules"
                },
                "logo_placement": {
                    "score": logo_placement_score,
                    "explanation": "Proper safe zone maintained" if logo_placement_score else f"Logo too close to edge (5px vs required {brand_data['safe_zone']})"
                },
                "logo_colors_compliance": {
                    "score": logo_color_score,
                    "explanation": "Logo colors correct" if logo_color_score else "Logo uses wrong accent color"
                }
            },
            "overall_feedback": "Compliance passed" if total_score>=2 else "Complianace check failed"
        }

    def check_compliance(self, image_path, brand_data):
        import time
        time.sleep(1.5)  
        return self.generate_mock_response(brand_data)