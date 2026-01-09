from controller.stats_controller import StatsController
from leaderboard import Leaderboard
from user import User

logged_in_user = None

while True:
    print("********** Login System **********")
    print("1.Signup")
    print("2.Login")
    print("3.Submit stats")
    print("4.Show leaderboard")
    print("5.View detailed match")
    print("6.Exit")

    ch = int(input("Enter your choice: "))
    if ch == 1:
        user = User("John", "Doe", "email@domain.com", 21, "M")
        user.signup()
    elif ch == 2:
        user = User("", "", "", "", "")
        logged_in_user = user.login()
    elif ch == 3:
        if not logged_in_user:
            print("Please login first!\n")
            continue
        sub = StatsController(logged_in_user["email"])
        match_id, stats_dict = sub.get_stats()
        if match_id:  # Only print if successful
            print(f"\nStats saved successfully!")
            print(f"Match ID: {match_id}")
            print(f"Goals: {stats_dict['goals']}, Assists: {stats_dict['assists']}")
    elif ch == 4:
        if not logged_in_user:
            print("Please login first!\n")
            continue
        Leaderboard.show_personal_leaderboard(logged_in_user["email"])
    elif ch == 5:
        if not logged_in_user:
            print("Please login first!\n")
            continue
        match_id = int(input("Enter match ID to view: "))
        Leaderboard.show_detailed_match(logged_in_user["email"], match_id)
    elif ch == 6:
        break
    else:
        print("Wrong Choice!")
