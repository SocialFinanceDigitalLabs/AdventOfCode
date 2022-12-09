# A very ASCII Christmas this year...

opening = """
             ____
          .-" +' "-.    __,  ,___,
         /.'.'A_'*`.\  (--|__| _, ,_  ,_
        |:.*'/\-\. ':|   _|  | (_| |_) |_) \ /
        |:.'.||"|.'*:|  (          |   |   _/
         \:~^~^~^~^:/            __,  ,___,
          /`-....-'\            (--|__| _ | '  _|  _,     ,
         /          \             _|  |(_)| | (_| (_| \ //_)
        `-., ____, .-'           (                    _/
"""

closing = """
   .-.                                                   \ /
  ( (                                |                  - * -
   '-`                              -+-                  / \\
            \            o          _|_          \\
            ))          }^{        /___\         ))
          .-#-----.     /|\     .---'-'---.    .-#-----.
     ___ /_________\   //|\\\\   /___________\  /_________\  
    /___\ |[] _ []|    //|\\\\    | A /^\ A |    |[] _ []| _.O,_
....|"#"|.|  |*|  |...///|\\\\\\...|   |"|   |....|  |*|  |..(^).... 
"""


def show_results(result, day):
    print(opening)
    print(" ╔════════════════════════════════════")
    print(" ║  *  *  *  *  * {} *  *  *  *".format(day.title()))
    print(" ╠════════════════════════════════════")
    for index, item in enumerate(result, start=1):
        print(" ║ The result for part {} is: {}".format(item["Part"], item["Value"]))
    print(" ╚════════════════════════════════════")
    print(closing)


def show_test_opener():
    print(" ┌────────────────────────────────────┐")
    print(" │ ▼▼▼▼▼▼▼  TESTING RESULTS  ▼▼▼▼▼▼▼  │")
    print(" └────────────────────────────────────┘")

def show_test_results(result, expected_result, test_name):
    try:
        assert result == expected_result
        print("               ╔════════╗")
        print(" ╔═════════════╝ {} ╚═════════════".format(test_name))
        print(" ║ Test PASSED")
        print(" ║ Expected {}, got {} ".format(expected_result, result))
        print(" ╚════════════════════════════════════")
    except AssertionError:
        print("               ╔════════╗")
        print(" ╔═════════════╝ {} ╚═════════════".format(test_name))
        print(" ║ Test FAILED!")
        print(" ║ Expected {}, got {} ".format(expected_result, result))
        print(" ╚════════════════════════════════════")
