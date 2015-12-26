from PinCreator import PinCreator

tokens = list()
tokens.append("SBwtoChHQTjHKiD3YkyFujhjO4OhyM4v")
tokens.append("UiL9JOZZHSuUNMkkztf7xJkf3cQ5CpNo")

for token in tokens:
    msg = "test1"
    pin1 = PinCreator(msg , hours = 1 , user_token=token)
    #pin1.addNotification("A new pin has been added")
    pin1.addReminder(msg)
    pin1.display()
    pin1.send()
