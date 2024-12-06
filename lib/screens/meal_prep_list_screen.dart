import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class MealPlanInputScreen extends StatefulWidget {
  const MealPlanInputScreen({Key? key}) : super(key: key);

  @override
  _MealPlanInputScreenState createState() => _MealPlanInputScreenState();
}

class _MealPlanInputScreenState extends State<MealPlanInputScreen> {
  final List<TextEditingController> _mealControllers = List.generate(7, (index) => TextEditingController());
  String result = "Enter your meal plan for the week.";

  Future<void> submitMealPlan() async {
    List<int> mealsPerWeek = _mealControllers.map((controller) => int.tryParse(controller.text) ?? 0).toList();

    try {
      final response = await http.post(
        Uri.parse('http://127.0.0.1:5000/validate_meal_plan'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'meals_per_week': mealsPerWeek}),
      );

      final responseData = jsonDecode(response.body);

      if (responseData['status'] == 'success') {
        setState(() {
          result = "Valid meal plan: ${responseData['meal_plan']}";
        });
      } else {
        setState(() {
          result = "Invalid meal plan: ${responseData['message']}";
        });
      }
    } catch (e) {
      setState(() {
        result = "Failed to submit meal plan. Please try again.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Meal Plan Input"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text("Enter the number of meals for each day of the week (2 or 3, or 0 for eating out):"),
            ...List.generate(7, (index) {
              return TextField(
                controller: _mealControllers[index],
                decoration: InputDecoration(
                  labelText: "Day ${index + 1}",
                ),
                keyboardType: TextInputType.number,
              );
            }),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: submitMealPlan,
              child: const Text("Submit Meal Plan"),
            ),
            const SizedBox(height: 20),
            Text(result),
          ],
        ),
      ),
    );
  }
}
