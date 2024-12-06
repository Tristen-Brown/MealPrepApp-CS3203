import 'package:flutter/material.dart';
import '../services/api_services.dart';

class MealPlanScreen extends StatefulWidget {
  const MealPlanScreen({Key? key}) : super(key: key);

  @override
  State<MealPlanScreen> createState() => _MealPlanScreenState();
}

class _MealPlanScreenState extends State<MealPlanScreen> {
  final List<TextEditingController> _controllers = List.generate(7, (_) => TextEditingController());
  String result = "";

  void validateMealPlan() async {
    final mealPlan = _controllers.map((controller) {
      return int.tryParse(controller.text) ?? -1; // -1 for invalid input
    }).toList();

    if (mealPlan.contains(-1)) {
      setState(() {
        result = "Please enter valid numbers for all days.";
      });
      return;
    }

    try {
      final response = await ApiService.validateMealPlan(mealPlan);
      setState(() {
        result = response['message'];
      });
    } catch (e) {
      setState(() {
        result = "Error: Unable to validate meal plan.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Meal Plan Validator")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            ...List.generate(7, (index) {
              return TextField(
                controller: _controllers[index],
                decoration: InputDecoration(labelText: "Meals for day ${index + 1} (2, 3, or 0 for eating out)"),
                keyboardType: TextInputType.number,
              );
            }),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: validateMealPlan,
              child: const Text("Validate Meal Plan"),
            ),
            const SizedBox(height: 20),
            Text(result, style: const TextStyle(fontSize: 16)),
          ],
        ),
      ),
    );
  }
}
