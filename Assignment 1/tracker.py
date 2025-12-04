# Author: Rishabh Bhardwaj
# Assignment Title: Daily Calorie Tracker CLI

import datetime
print("\n\t---Daily Calorie Tracker CLI---")
print("This tool helps you log your meals and track your total daily calorie intake.")
print("------------------------------------------------------------------------\n")
meal_names = []
calorie_amounts = []
while True:
    try:
        num_meals = int(input("How many meals do you want to enter? "))
        if num_meals < 1:
            print("Please enter at least one meal.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a whole number.")

for i in range(num_meals):
    print(f"\n--- Entering Meal #{i + 1} ---")
    name = input("Enter meal name (e.g., Breakfast, Lunch): ")
    meal_names.append(name)
    while True:
        try:
            calories = float(input(f"Enter calories for {name}: "))
            if calories <= 0:
                print("Calories cannot be negative. Try again.")
                continue
            calorie_amounts.append(calories)
            break
        except ValueError:
            print("Invalid input. Please enter a number for calories.")

total_calories = sum(calorie_amounts)
if num_meals > 0:
    average_calories = total_calories / num_meals
else:
    average_calories = 0
while True:
    try:
        daily_limit = float(input("\nWhat is your daily calorie limit? "))
        if daily_limit <=0:
            print("Limit cannot be negative. Try again.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a number for your limit.")
    
print("\n--- Limit Status ---")
if total_calories > daily_limit:
    excess = total_calories - daily_limit
    print(f"WARNING! You have exceeded your daily limit of {daily_limit:.2f} calories.")
    print(f"You are over the limit by {excess:.2f} calories.")
elif total_calories == daily_limit:
    print(f"CONGRATS! You hit your daily limit of {daily_limit:.2f} calories exactly.")
else:
    remaining = daily_limit - total_calories
    print(f"SUCCESS! You are still within your daily limit of {daily_limit:.2f} calories.")
    print(f"You have {remaining:.2f} calories remaining today.")

print("\n" + "="*50)
print("\t\tDAILY CALORIE SUMMARY REPORT")
print("="*50)
print(f"Date/Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nMeal Name\t\tCalories") 
print("---------------------------------") 

for name, calories in zip(meal_names, calorie_amounts):
    print(f"{name}:\t\t\t{calories:.2f}")
print("---------------------------------") 
print(f"TOTAL:\t\t\t{total_calories:.2f}")
print(f"AVERAGE:\t\t{average_calories:.2f}")
print("="*50)

save_log = input("\nDo you want to save this report to a file (y/n)? ").lower()
if save_log == 'y':
    filename = "calorie_log.txt"
    try:
        with open(filename, "w") as file:
            file.write("DAILY CALORIE TRACKER SESSION LOG\n")
            file.write(f"Timestamp: {datetime.datetime.now()}\n")
            file.write(f"Daily Calorie Limit Set: {daily_limit:.2f}\n\n")
            
            file.write("--- Meal Details ---\n")
            file.write("Meal Name\t\tCalories\n")
            file.write("---------------------------------\n")
            for name, calories in zip(meal_names, calorie_amounts):
                file.write(f"{name}:\t\t{calories:.2f}\n")
            
            file.write("---------------------------------\n")
            file.write(f"TOTAL CALORIES CONSUMED: {total_calories:.2f}\n")
            file.write(f"AVERAGE CALORIES PER MEAL: {average_calories:.2f}\n")
            file.write(f"Limit Status: {'EXCEEDED' if total_calories > daily_limit else 'WITHIN LIMIT'}\n")
            
        print(f"Report saved successfully to {filename}!")
    except IOError:
        print(f"Error: Could not write to file {filename}.")

print("\nKeep Being Healthy!")
