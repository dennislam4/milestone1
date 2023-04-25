import datetime


def get_stats():
    """
    Gets the user's physical body information that is needed for calculations. Height and weight are asked in
    imperial units and then converted into metric for the sake of computation.
    """
    print("Please provide the following information:")
    age = int(input("Enter your age: "))
    gender = input("Enter your gender (M/F): ").upper()
    height_ft = int(input("Enter your height in feet: "))
    height_in = int(input("Enter your remaining height in inches: "))
    # Convert height to centimeters
    height = (height_ft * 12 + height_in) * 2.54
    weight_lb = float(input("Enter your weight in pounds: "))
    # Convert weight to kilograms
    weight = weight_lb * 0.453592
    bmr = calculate_bmr(gender, weight, height, age)
    adjusted_bmr = get_weight_goal(bmr)
    return {
        "age": age,
        "gender": gender,
        "height": height,
        "weight": weight,
        "bmr": adjusted_bmr,
    }


def calculate_bmr(gender, weight, height, age):
    """
    Calculates the user's Basal metabolic rate using the Mifflin-St Jeor Equation.
    """
    # If the user is male, the men's calculation is conducted
    if gender == "M":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    # Otherwise, the user is female and the women's calculation is conducted
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmr


def get_weight_goal(bmr):
    """
    Returns the target daily calorie intake based on the user's choice. Uses the calculated user bmr as a parameter.
    """
    print("\nChoose your weight goal:")
    print("1. Lose weight")
    print("2. Maintain weight")
    print("3. Gain weight")
    choice = int(input("Enter your choice (1, 2, or 3): "))
    # If the user wants to lose weight, then they are returned their original BMR
    if choice == 1:
        return bmr
    # If the user wants to maintain weight, 150 kcal is added to their BMR
    elif choice == 2:
        return bmr + 150
    # If the user wants to gain weight, 500 kcal is added to their BMR
    elif choice == 3:
        return bmr + 500
    else:
        print("Invalid choice. Please try again.")
        return get_weight_goal(bmr)


def log_weight(weight_logs):
    """
    Users enter information to log table which records their weight and calorie intake.
    """
    date_str = input("Enter the date (yyyy-mm-dd): ")
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    weight_lb = float(input("Enter your weight in pounds: "))
    weight = weight_lb * 0.453592  # Convert to kg
    calories = float(input("Enter your daily calorie intake (kcal): "))
    weight_log = {
        "date": date,
        "weight": weight,
        "calories": calories,
    }
    weight_logs.append(weight_log)


def view_weight_logs(weight_logs):
    """
    Text based table used to view user entries.
    """

    print("\nDate       Weight (lbs)  Calories (kcal)")
    print("-----------------------------------------")

    for log in weight_logs:
        weight_lb = log['weight'] / 0.453592
        print(f"{log['date']}   {weight_lb:.2f}       {log['calories']}")


def display_fitness_goal_details(fitness_goal):
    """
    Gathers the calculated values of and displays the user their stats and daily calorie intake for their goal.
    """
    print("\nYour personal details and fitness goal:")
    for key, value in fitness_goal.items():

        if key == 'height':
            height_ft = int(value // 30.48)
            height_in = int((value % 30.48) / 2.54)
            print(f"Height: {height_ft} ft {height_in} in")
        elif key == 'weight':
            weight_lb = value / 0.453592
            print(f"Weight: {weight_lb:.2f} lbs")
        elif key == 'bmr':
            print(f"Your daily calorie intake for your goal is estimated to be: {value:.2f} kcal")
        else:
            print(f"{key.capitalize()}: {value}")


def create_custom_workout_plan(workout_days):
    """
    Users are able to enter their own workouts along with their names, number of reps, number of sets, and
    how many workouts per week.zX
    """
    custom_plan = {}

    for week in range(1, 13):
        custom_plan[week] = []

        for day in range(1, workout_days + 1):
            print(f"\nWeek {week}, Day {day}:")
            num_exercises = int(input("Enter the number of exercises for this day: "))
            day_exercises = []

            for i in range(1, num_exercises + 1):
                print(f"\nExercise {i}:")
                exercise = input("Enter the exercise: ")
                sets = int(input("Enter the number of sets: "))
                reps = int(input("Enter the number of reps: "))
                day_exercises.append({
                    "exercise": exercise,
                    "sets": sets,
                    "reps": reps,
                })
            custom_plan[week].append(day_exercises)
    return custom_plan


def generate_workout_plan(workout_days):
    """
    Used to create predetermined workout plan for the user based on the number of days they choose. Cycles through
    the list of 6 predetermined areas to work out.
    """
    choice = int(input("Enter 1 to use the pre-defined workout plan or 2 to create your own: "))
    if choice == 1:
        workout_exercises = ["Cardio", "Upper body", "Lower body", "Core", "Cardio", "Full body", ]
        print("\nYour 12-week workout plan:")

        for weeks in range(1, 13):
            print(f"\nWeek {weeks}:")

            for days in range(1, workout_days + 1):
                exercise = workout_exercises[(weeks + days - 2) % len(workout_exercises)]
                print(f"  Day {days}: {exercise} - 3 sets of 10 reps")

    elif choice == 2:
        custom_plan = create_custom_workout_plan(workout_days)
        print("\nYour custom 12-week workout plan:")

        for weeks, days in custom_plan.items():
            print(f"\nWeek {weeks}:")

            for day, workout in enumerate(days, start=1):
                print(f"  Day {day}: {workout['exercise']} - {workout['sets']} sets of {workout['reps']} reps")

    else:
        print("Invalid choice. Please try again.")
        generate_workout_plan(workout_days)


def main():
    stats = get_stats()
    display_fitness_goal_details(stats)

    weight_logs = []
    while True:
        print("\nOptions:")
        print("1. Log weight and calories")
        print("2. View weight logs")
        print("3. Generate workout plan")
        print("4. Quit")

        choice = int(input("Enter your choice (1, 2, 3, or 4): "))

        if choice == 1:
            log_weight(weight_logs)
        elif choice == 2:
            view_weight_logs(weight_logs)
        elif choice == 3:
            workout_days = int(input("Enter the number of workout days per week (1-6): "))
            if 1 <= workout_days <= 6:
                generate_workout_plan(workout_days)
            else:

                print("Invalid input. Please enter a number between 1 and 6.")

        elif choice == 4:
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
