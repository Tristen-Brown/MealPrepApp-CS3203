import 'package:flutter/material.dart';
import '../services/nutrition_service.dart';

class MacrosCalculatorScreen extends StatefulWidget {
  const MacrosCalculatorScreen({Key? key}) : super(key: key);

  @override
  State<MacrosCalculatorScreen> createState() => _MacrosCalculatorScreenState();
}

class _MacrosCalculatorScreenState extends State<MacrosCalculatorScreen> {
  final TextEditingController _foodController = TextEditingController();
  final TextEditingController _servingSizeController = TextEditingController();
  String result = "Enter food item and serving size";

  void calculateMacros() async {
    final foodItem = _foodController.text;
    final servingSize = _servingSizeController.text;

    if (foodItem.isEmpty || servingSize.isEmpty) {
      setState(() {
        result = "Please enter both a food item and a serving size.";
      });
      return;
    }

    final foodQuery = "$servingSize of $foodItem";
    final nutritionData = await NutritionService.getNutritionData(foodQuery);

    if (nutritionData != null) {
      setState(() {
        result = '''
Calories: ${nutritionData['calories']}
Protein: ${nutritionData['protein']}g
Carbs: ${nutritionData['carbs']}g
Sugar: ${nutritionData['sugar']}g
Fat: ${nutritionData['fat']}g
        ''';
      });
    } else {
      setState(() {
        result = "Failed to fetch nutrition data.";
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Macros Calculator"),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _foodController,
              decoration: const InputDecoration(
                labelText: "Enter food item (e.g., Chicken Breast)",
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _servingSizeController,
              decoration: const InputDecoration(
                labelText: "Enter serving size (e.g., 200g or 2 cups)",
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: calculateMacros,
              child: const Text("Calculate Macros"),
            ),
            const SizedBox(height: 20),
            Text(result),
          ],
        ),
      ),
    );
  }
}
