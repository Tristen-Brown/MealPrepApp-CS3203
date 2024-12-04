import 'package:flutter/material.dart';
import '../services/api_services.dart';

class MealRecommendationScreen extends StatefulWidget {
  const MealRecommendationScreen({Key? key}) : super(key: key);

  @override
  State<MealRecommendationScreen> createState() => _MealRecommendationScreenState();
}

class _MealRecommendationScreenState extends State<MealRecommendationScreen> {
  final TextEditingController _ingredientController = TextEditingController();
  String recommendations = "Enter ingredients to get meal recommendations.";

  void fetchRecommendations() async {
    final ingredients = _ingredientController.text.split(',').map((e) => e.trim()).toList();
    if (ingredients.isEmpty) {
      setState(() {
        recommendations = "Please enter at least one ingredient.";
      });
      return;
    }
    try {
      final data = await ApiService.getMealRecommendations(ingredients);
      setState(() {
        recommendations = data.map((rec) => rec['name']).join("\n");
      });
    } catch (e) {
      setState(() {
        recommendations = "Failed to fetch recommendations. Please try again.";
      });
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
          children: [
            TextField(
              controller: _ingredientController,
              decoration: const InputDecoration(
                labelText: "Enter ingredients (comma-separated)",
              ),
            ),
            const SizedBox(height: 10),
            ElevatedButton(
              onPressed: fetchRecommendations,
              child: const Text("Get Recommendations"),
            ),
            const SizedBox(height: 20),
            Text(recommendations),
          ],
        ),
      ),
    );
  }
}
