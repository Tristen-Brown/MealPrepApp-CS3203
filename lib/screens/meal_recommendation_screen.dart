import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class MealRecommendationScreen extends StatefulWidget {
  const MealRecommendationScreen({super.key});

  @override
  State<MealRecommendationScreen> createState() => _MealRecommendationScreenState();
}

class _MealRecommendationScreenState extends State<MealRecommendationScreen> {
  final TextEditingController _ingredientsController = TextEditingController();
  List<Map<String, dynamic>> _recommendations = [];

  Future<void> getMealRecommendations() async {
  final ingredientsText = _ingredientsController.text.trim();
  if (ingredientsText.isEmpty) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text("Please enter at least one ingredient.")),
    );
    return;
  }

  final ingredients = ingredientsText.split(',').map((e) => e.trim()).toList();
  final url = Uri.parse('http://127.0.0.1:5000/recipe_generation'); // Replace with your local IP if necessary

  try {
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'ingredients': ingredients}),
    );

    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      // Log data to debug
      print("Response data: $data");

      if (data != null && data['recipe'] != null && data['recipe'] is List && data['recipe'].isNotEmpty) {
        setState(() {
          _recommendations = List<Map<String, dynamic>>.from(data['recipe']);
        });
      } else {
        setState(() {
          _recommendations = [];
        });
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("No recipes found. Try using different ingredients or check your internet connection.")),
        );
      }

    } else {
      // Show error response from the server
      final errorResponse = jsonDecode(response.body);
      print("Error response: $errorResponse");

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Failed to get meal recommendations: ${errorResponse['error']}")),
      );
    }
  } catch (e) {
    print("Exception caught: $e");

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text("Error: $e")),
    );
  }
}





  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Meal Recommendations"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            TextField(
              controller: _ingredientsController,
              decoration: const InputDecoration(
                labelText: "Enter Ingredients (comma-separated)",
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: getMealRecommendations,
              child: const Text("Get Meal Recommendations"),
            ),
            const SizedBox(height: 20),
            _recommendations.isNotEmpty
                ? Expanded(
                    child: ListView.builder(
                      itemCount: _recommendations.length,
                      itemBuilder: (context, index) {
                        final recommendation = _recommendations[index];
                        return Card(
                          margin: const EdgeInsets.symmetric(vertical: 5),
                          child: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  recommendation['recipe name'] ?? 'Unnamed Recipe',
                                  style: const TextStyle(
                                    fontWeight: FontWeight.bold,
                                    fontSize: 18,
                                  ),
                                ),
                                const SizedBox(height: 5),
                                Text(
                                  "Ingredients:",
                                  style: const TextStyle(fontWeight: FontWeight.bold),
                                ),
                                ...List<Widget>.from(
                                  (recommendation['ingredients'] as List).map(
                                    (ingredient) => Text("- $ingredient"),
                                  ),
                                ),
                                const SizedBox(height: 5),
                                Text(
                                  "Instructions:",
                                  style: const TextStyle(fontWeight: FontWeight.bold),
                                ),
                                ...List<Widget>.from(
                                  (recommendation['instructions'] as List).map(
                                    (instruction) => Text("- $instruction"),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
                  )
                : const Text("No recommendations yet. Enter ingredients to get started."),
          ],
        ),
      ),
    );
  }
}
