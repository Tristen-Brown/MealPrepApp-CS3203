import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String apiUrl = "http://10.204.106.237:5000/recipe_generation"; // Replace with your local IP

  static Future<List<Map<String, dynamic>>> generateRecipes(List<String> ingredients) async {
    final response = await http.post(
      Uri.parse(apiUrl),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'ingredients': ingredients}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return List<Map<String, dynamic>>.from(data['recipes']);
    } else {
      throw Exception('Failed to generate recipes: ${response.body}');
    }
  }
}