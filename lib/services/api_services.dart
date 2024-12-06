import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String generationApiUrl = "http://10.204.106.237:5000/recipe_generation"; // Replace with your local IP

  static Future<List<Map<String, dynamic>>> generateRecipes(List<String> ingredients) async {
    final response = await http.post(
      Uri.parse(generationApiUrl),
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

  static const String backendUrl = 'http://127.0.0.1:5000';

  static Future<Map<String, dynamic>> validateRestrictions(String restrictions) async {
    final response = await http.post(
      Uri.parse('$backendUrl/validate_restrictions'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'restrictions': restrictions}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to validate restrictions');
    }
  }

  static const String baseUrl = "http://127.0.0.1:5000";

  static Future<Map<String, dynamic>> validateMealPlan(List<int> mealPlan) async {
    final response = await http.post(
      Uri.parse('$baseUrl/validate_meal_plan'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'meal_plan': mealPlan}),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception("Failed to validate meal plan");
    }
  }
}