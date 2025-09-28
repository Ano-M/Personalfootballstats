from stats_submission import StatsSubmission
from leaderboard import Leaderboard
from user import User

logged_in_user = None

while True:
    print("********** Login System **********")
    print("1.Signup")
    print("2.Login")
    print("3.Submit stats")
    print("4.Show leaderboard")
    print("5.Exit")

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
        sub = StatsSubmission(logged_in_user["email"], "", "", "")
        match_id, goals, assists, date = sub.get_stats()
        print(f"Stats entered: Goals={goals}, Assists={assists}, Date={date}")
    elif ch == 4:
        if not logged_in_user:
            print("Please login first!\n")
            continue
        Leaderboard.show_personal_leaderboard(logged_in_user["email"])
    elif ch == 5:
        break
    else:
        print("Wrong Choice!")
