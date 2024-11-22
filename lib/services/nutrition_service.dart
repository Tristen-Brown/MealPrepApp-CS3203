import 'dart:convert';
import 'package:http/http.dart' as http;

class NutritionService {
  static const String apiUrl = "https://trackapi.nutritionix.com/v2/natural/nutrients";
  static const String appId = "8bc7b25a"; // Replace with your actual API ID
  static const String appKey = "dd56c0e7590da1e3f54f9269de8b9588"; // Replace with your actual API Key

  // Fetch nutrition data from Nutritionix
  static Future<Map<String, dynamic>?> getNutritionData(String foodQuery) async {
    final headers = {
      'Content-Type': 'application/json',
      'x-app-id': appId,
      'x-app-key': appKey,
    };

    final body = jsonEncode({'query': foodQuery});

    try {
      final response = await http.post(Uri.parse(apiUrl), headers: headers, body: body);

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        final firstFood = data['foods'][0];

        return {
          'calories': firstFood['nf_calories'] ?? 0,
          'protein': firstFood['nf_protein'] ?? 0,
          'carbs': firstFood['nf_total_carbohydrate'] ?? 0,
          'sugar': firstFood['nf_sugars'] ?? 0,
          'fat': firstFood['nf_total_fat'] ?? 0,
        };
      } else {
        print('Error: ${response.statusCode}');
        return null;
      }
    } catch (e) {
      print('Exception: $e');
      return null;
    }
  }
}
