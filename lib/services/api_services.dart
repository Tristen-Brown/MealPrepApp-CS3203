import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static Future<List<dynamic>> getMealRecommendations(List<String> ingredients) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/meal_recommendation'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'ingredients': ingredients}),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body)['recommendations'];
    } else {
      throw Exception('Failed to fetch meal recommendations');
    }
  }
}