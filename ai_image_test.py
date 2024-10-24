import unittest
from unittest.mock import patch
import requests
from app import upload_image, send_image_to_ai, handle_ai_response, get_recipe_suggestions, submit_feedback
from PIL import Image
import io

class TestImageUpload(unittest.TestCase):
    
    # Create dummy image for testing
    def setUp(self):
        self.image = Image.new("RGB", (100, 100), color="blue")
        img_byte_arr = io.BytesIO()
        self.image.save(img_byte_arr, format="JPEG")
        self.image_data = img_byte_arr.getvalue()

    # Test uploading valid image
    def test_upload_valid_image(self):
        response = upload_image(self.image_data)
        self.assertEqual(response.status_code, 200, "Image upload failed")
        self.assertIn("success", response.json(), "Upload not successful")

class TestImageFormatValidation(unittest.TestCase):
   
    # Create valid and invalid images for testing
    def setUp(self):
        self.valid_image = Image.new("RGB", (100, 100), color="blue")
        self.invalid_file = b"This is a test file, not an image."

        img_byte_arr = io.BytesIO()
        self.valid_image.save(img_byte_arr, format="JPEG")
        self.valid_image_data = img_byte_arr.getvalue()
    
    # Test valid image format (JPEG)
    def test_upload_valid_image_format(self):
        response = upload_image(self.valid_image_data)
        self.assertEqual(response.status_code, 200, "Valid image upload failed")
    
    # Test invalid file format (not an image)
    def test_upload_invalid_image_format(self):
        response = upload_image(self.invalid_file)
        self.assertEqual(response.status_code, 400, "Invalid file accepted")

class TestAiFetch(unittest.TestCase):

    @patch('app.requests.post')
    def test_fetch_ai_api(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ingredients": ["eggs", "milk", "flour"]}

        response = requests.post('https://api.example.com/process_image', data={"image": "fake_image_data"})
        self.assertEqual(response.status_code, 200, "AI API fetch failed")
        self.assertIn("ingredients", response.json(), "AI API response missing ingredients")

class TestImageTransmission(unittest.TestCase):

    @patch('app.requests.post')
    def test_send_image_to_ai(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ingredients": ["eggs", "milk"]}

        image_data = b"fake_image_data"

        response = send_image_to_ai(image_data)

        self.assertEqual(response.status_code, 200, "Failed to send image to AI API")
        self.assertIn("ingredients", response.json(), "AI response does not contain ingredients")

        mock_post.assert_called_once_with('https://api.example.com/process_image', files={'image': image_data})

class TestAIResponseHandling(unittest.TestCase):
    
    @patch('app.requests.post')
    def test_handle_ai_response(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ingredients": ["tomatoes", "cheese", "bread"]}

        response = requests.post('https://api.example.com/process_image', data={"image": "fake_image_data"})
        result = handle_ai_response(response.json)

        self.assertEqual(result, ["tomatoes", "cheese", "bread"], "Incorrect ingredients list returned from AI response")

class TestIngredientRecognitionAccuracy(unittest.TestCase):

    @patch('app.requests.post')
    def test_ingredient_recognition_accuracy(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ingredients": ["carrots", "potatoes", "chicken"]}

        image_data = b"fake_image_data"

        response = send_image_to_ai(image_data)
        ingredients = handle_ai_response(response.json())

        self.assertEqual(ingredients, ["carrots", "potatoes", "chicken"])

class TestRecipeSuggestion(unittest.TestCase):

    @patch('app.get_recipe_suggestions')
    def test_recipe_suggestion(self, mock_get_recipes):
        mock_get_recipes.return_value = ["Carrot Soup", "Chicken Stir Fry"]

        ingredients = ["carrots", "potatoes", "chicken"]

        recipes = get_recipe_suggestions(ingredients)

        self.assertIn("Carrot Soup", recipes, "Recipe suggestion based on ingredients failed")
        self.assertIn("Chicken Stir Fry", recipes, "Recipe suggestion based on ingredients failed")

class TestIncompleteImageHandling(unittest.TestCase):

    @patch('app.requests.post')
    def test_incomplete_image_handling(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"ingredients": []}

        image_data = b"blurry_image_data"

        response = send_image_to_ai(image_data)

        self.assertEqual(response.json()["ingredients"], [], "AI should not recognize ingredients from a poor-quality image")

class TestUserFeedback(unittest.TestCase):

    @patch('app.submit_feedback')
    def test_feedback_on_incorrect_suggestions(self, mock_feedback):
        mock_feedback.return_value.status_code = 200
        mock_feedback.return_value.json.return_value = {"status": "success", "message": "Feedback submitted"}

        feedback_data = {
            "ingredients": "potato",
            "issue": "Incorrectly recognized"
        }

        response = submit_feedback(feedback_data)

        self.assertEqual(response.status_code, 200, "Feedback submission failed")
        self.assertIn("success", response.json()["status"], "Feedback submission was not successful")


if __name__ == '__main__':
    unittest.main()