import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static Future<Map<String, dynamic>> calculateMacros(List<Map<String, dynamic>> ingredients) async {
    final response = await http.post(
      Uri.parse('http://127.0.0.1:5000/calculate_macros'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'ingredients': ingredients}),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    } else {
      throw Exception('Failed to calculate macros');
    }
  }
}
