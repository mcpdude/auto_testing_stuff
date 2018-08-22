import pigpio

pi = pigpio.pi()

pins = {
    "1": "18",
    "2": "3", # Ken messed this up, yell at him if it borks
    "3": "4",
    "4": "17",
    "5": "27",
    "6": "22",
    "7": "23",
    "8": "24",
    "9": "25",
    "10": "5",
    "11": "6",
    "12": "13",
    "13": "19",
    "14": "26",
    "15": "12",
    "16": "16"

}

todo = ""
which = ""


while todo != "quit":
    todo = input("Turn the relays on or off?")

    if todo == "on":
        which = input("Which one? Type all to turn them all on.\n")
        if which == "all":
            print("this don't work, sorry")

        else:
            print("Turning on relay:", which, "GPIO:",  pins.get(which, ""))
            pi.set_mode(int(pins.get(which, "")), pigpio.OUTPUT)
            pi.write(int(pins.get(which, "")), 1)
            print("Turned on the relay.")



    elif todo == "off":
        which = input("Which one? Type all to turn them all on.\n")
        if which == "all":
            print("this don't work, sorry")

        else:
            print("Turning off relay:", which, "GPIO:",  pins.get(which, ""))
            #pi.set_mode(int(which), pigpio.OUTPUT)
            pi.write(int(pins.get(which, "")), 0)            
            print("Turned off the relay.")

    elif todo =="quit":
        break
