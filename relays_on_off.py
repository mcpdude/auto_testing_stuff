from gpiozero import LED
pin14 = LED(14)
pin15 = LED(15)
pin18 = LED(18)
pin23 = LED(23)
todo = ""

while todo != "quit":
    todo = input("Turn the relays on or off?")

    if todo == "on":
        print("Turning the relays on.")
        pin14.on()
        pin15.on()
        pin18.on()
        pin23.on()

    elif todo == "off":
        print("Turning the relays off.")
        pin14.off()
        pin15.off()
        pin18.off()
        pin23.off()

    elif todo =="quit":
        break


