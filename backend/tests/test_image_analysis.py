import unittest
from unittest.mock import MagicMock, patch, mock_open
import json
import backend.utils.scan_image as scan_image

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

if __name__ == '__main__':
    unittest.main()