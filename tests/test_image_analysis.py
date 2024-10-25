import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
import image_uploader

class TestImageAnalysis(unittest.TestCase):
    
    def setUp(self):
        # Create a mock response similar to the structure you're receiving
        self.mock_response = MagicMock()
        self.mock_response.result.candidates[0].content.parts[0].text = (
            "```json\n"
            "{\n"
            "    \"All ingredients\": [\"eggs\", \"milk\"],\n"
            "    \"Recipes\": [{\"recipe name\": \"Sample Recipe\", \"ingredients\": [\"eggs\"], \"instructions\": \"Mix ingredients.\"}]\n"
            "}\n"
            "```"
        )

    def test_json_format(self):
        # Extract the JSON from the mocked response using your function
        json_text = self.mock_response.result.candidates[0].content.parts[0].text
        # Perform similar text processing as in your function
        if json_text.startswith("```json"):
            json_text = json_text[7:]  # Remove the ```json\n at the beginning
        if json_text.endswith("```"):
            json_text = json_text[:-3]  # Remove the ``` at the end

        # Check if the extracted text can be parsed as JSON
        try:
            data = json.loads(json_text)
            self.assertIsInstance(data, dict)  # Ensure the result is a dictionary (JSON object)
        except json.JSONDecodeError:
            self.fail("The response is not a valid JSON format")
    
    # def test_image_analysis(self):
    #     mock_response = MagicMock()

    #     mock_response.json.return_value = {  # Changed to a dictionary
    #         'All ingredients': ["tomatoes", "cheese", "lettuce", "chicken", "bread"],
    #         "Recipes": [
    #             {
    #                 "reciope name": "Grilled Chicken Salad",
    #                 "ingredients_needed": ["chicken", "lettuce", "tomato"],
    #                 "instructions": "Mix chicken, lettuce, and tomato. Add dressing.",
    #             },
    #             {
    #                 "recipe name": "Cheese and Tomato Sandwich",
    #                 "ingredients_needed": ["cheese", "tomato", "bread"],
    #                 "instructions": "Place cheese and tomato between two slices of bread and grill.",
    #             },
    #             {
    #                 "recipe name": "Grilled Cheese",
    #                 "ingredients": ["cheese", "bread"],
    #                 "instructions": "Place cheese between two slices of bread and grill."
    #             }
    #         ]
    #     }


    #     mock_response.return_value = mock_response

    #     # with open('test_json.json', 'r') as f:
    #     #     response = json.load(f)

    #     response = image_uploader.upload_image('test_image2.jpg')

    #     ingredients = response['All ingredients']
    #     self.assertIn('lettuce', ingredients)
    #     self.assertIn('green pepper', ingredients)
    #     self.assertIn('eggs', ingredients)
    #     self.assertIn('tomatoes', ingredients)
    #     self.assertIn('carrots', ingredients)

    #     recipes = response['Recipes']
    #     self.assertEqual(len(recipes), 3) 
    #     self.assertEqual(recipes[0]['reciope name'], 'Greek Salad')
    #     self.assertEqual(recipes[1]['recipe name'], 'Pasta Primavera')
    #     self.assertEqual(recipes[2]['recipe name'], 'Avocado Toast')

if __name__ == '__main__':
    unittest.main()