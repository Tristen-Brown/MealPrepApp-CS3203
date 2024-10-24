import unittest
from unittest.mock import MagicMock, patch, mock_open
import image_uploader

class TestImageAnalysis(unittest.TestCase):

    @patch ('image_uploader.requests.post')
    @patch('builtins.open', new_callable=mock_open, read_data="mocked image data")
    def test_image_analysis_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success", 
            "message": "Analysis complete",
            "data": {
                "ingredients": ["tomatoes", "cheese", "lettuce", "chicken", "bread"],
                "recipes": [
                    {
                        "name": "Grilled Chicken Salad",
                        "instructions": "Mix chicken, lettuce, and tomato. Add dressing.",
                        "ingredients_needed": ["chicken", "lettuce", "tomato"]
                    },
                    {
                        "name": "Cheese and Tomato Sandwich",
                        "instructions": "Place cheese and tomato between two slices of bread and grill.",
                        "ingredients_needed": ["cheese", "tomato", "bread"]
                    }
                ]
            }}
        mock_response.return_value = mock_response

        response = image_uploader.upload_image('image-file-path')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Check that ingredients are correctly identified
        ingredients = response.json()['data']['ingredients']
        self.assertIn('tomato', ingredients)
        self.assertIn('cheese', ingredients)
        self.assertIn('lettuce', ingredients)
        self.assertIn('chicken', ingredients)
        self.assertIn('bread', ingredients)

        # Check that recipes are correctly suggested
        recipes = response.json()['data']['recipes']
        self.assertEqual(len(recipes), 2)  # Two recipes suggested
        self.assertEqual(recipes[0]['name'], 'Grilled Chicken Salad')
        self.assertEqual(recipes[1]['name'], 'Cheese and Tomato Sandwich')

        # Check that the first recipe includes the expected ingredients
        recipe_ingredients = recipes[0]['ingredients_needed']
        self.assertIn('chicken', recipe_ingredients)
        self.assertIn('lettuce', recipe_ingredients)
        self.assertIn('tomato', recipe_ingredients)

        recipe_ingredients = recipes[1]['ingredients_needed']
        self.assertIn('cheese', recipe_ingredients)
        self.assertIn('tomato', recipe_ingredients)
        self.assertIn('bread', recipe_ingredients)

    @patch('image_uploader.requests.post')
    def test_image_analysis_failure(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "status": "failed",
            "message": "Invalid image format"
        }

        mock_post.return_value = mock_post

        response = image_uploader.upload_image('image-file-path')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'failed')
        self.assertEqual(response.json()['message'], "Invalid image format")

if __name__ == '__main__':
    unittest.main()