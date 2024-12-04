# Maximum meals per day
MAX_MEALS_PER_DAY = 3  # Will pass 2 and 3 meals, but fail for anything higher
MAX_EATING_OUT_DAYS = 1  # Only one day can be "eating out" (meals_per_day = 0)

# Meal selection function
def validate_meal_selection(meals_per_day, eating_out=False):
    # If the user selects to eat out, meals_per_day should be 0
    if eating_out:
        return meals_per_day == 0
    
    # Valid meal selection: 2 or 3 meals per day
    return 2 <= meals_per_day <= MAX_MEALS_PER_DAY

# Function to get user input and validate meal selection for a week
def get_user_input_and_validate():
    while True:  # Restart the input process if "no" is chosen
        # Ask for meals per day for the 7 days of the week
        meals_per_week = []
        eating_out_count = 0
        valid_input = True  # To track if the entire input is valid

        for i in range(7):
            while True:  # Keep asking until a valid input is entered
                try:
                    # Get input from the user for the number of meals for the day
                    meals_per_day = int(input(f"Enter the number of meals for day {i + 1} (2 or 3, or 0 for eating out): "))
                    
                    if meals_per_day == 0:  # Check for eating out day
                        if eating_out_count < MAX_EATING_OUT_DAYS:
                            meals_per_week.append(meals_per_day)
                            eating_out_count += 1
                            break  # Valid input, move on to next day
                        else:
                            print("You can only eat out one day a week. Please enter a valid number of meals.")
                    elif validate_meal_selection(meals_per_day):
                        meals_per_week.append(meals_per_day)
                        break  # Valid input, move on to next day
                    else:
                        print("Invalid input. Please enter 2 or 3 meals per day.")
                        correct_input = input("Do you want to correct the input? (yes/no): ").strip().lower()
                        if correct_input != "yes":
                            print("Test failed! Invalid input will reset the process.")
                            valid_input = False
                            break  # Exit the loop to restart the process
                        else:
                            # Ask for correction if the user chooses 'yes'
                            continue

                except ValueError:
                    print("Invalid input. Please enter a valid number of meals.")
                    correct_input = input("Do you want to correct the input? (yes/no): ").strip().lower()
                    if correct_input != "yes":
                        print("Test failed! Invalid input will reset the process.")
                        valid_input = False
                        break  # Exit the loop to restart the process
                    else:
                        continue

            if not valid_input:
                break  # Exit the outer loop to restart the input process

        # If the input is valid for the whole week, break the loop and show the results
        if valid_input:
            print("Meal plan for the week:", meals_per_week)
            
            # Check if the plan is valid
            if eating_out_count == 1:
                print("Test passed! Valid meal plan with one eating out day.")
                break  # Exit the loop, successful meal plan
            else:
                print("Test failed! You need exactly one day of eating out.")
                continue  # Restart the input process if eating out days are not correct

# Running the validation function
if __name__ == '__main__':
    get_user_input_and_validate()
