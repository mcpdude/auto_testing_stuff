from gpiozero import LED
pins = {
    "1": "18",
    "2": "3", # Ken messed this up, yell at him if it borks
    "3": "4",
    "4": "17",
    "5": "27",
    "6": "22",
    "7": "23",
    "8": "24",
    "9": "24",
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
            switch = LED(int(pins.get(which, ""))
            switch.on()
            print("Turned on the relay.")



    elif todo == "off":
        print("Turning the relays off.")
        pin14.on()
        pin15.on()
        pin18.on()
        pin23.on()
        pin14.off()
        pin15.off()
        pin18.off()
        pin23.off()

    elif todo =="quit":
        break
