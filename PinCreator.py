#https://developer.getpebble.com/guides/timeline/pin-structure/
#https://github.com/youtux/pypebbleapi/tree/master/pypebbleapi

from pypebbleapi import Timeline
import datetime
import pprint
import copy

timeline = Timeline()

generic_reminder = dict(
    time=" ",
    layout=dict(
        type="genericReminder",
        title=" ",
        tinyIcon="system://images/ALARM_CLOCK",
    )
)

generic_notification = dict(
    layout = dict(
        type="genericNotification",
        title=" ",
        body=" ",
        tinyIcon="system://images/NOTIFICATION_GENERIC"
    )
)

generic_layout = dict(
    type="genericPin",
    title=" ",
    subtitle=" ",
    body=" ",
    tinyIcon="system://images/NOTIFICATION_FLAG",
)

generic_action = dict(
    type="http",
    title=" ",
    url=" ",
    method="POST",
    bodyJSON=dict(),
    successIcon="system://images/GENERIC_CONFIRMATION",
    successText=" "
)
    
class PinCreator:
    def __init__(self, title, subtitle=None, body=None, hours=0, minutes=0, user_token="SBwtoChHQTjHKiD3YkyFujhjO4OhyM4v"):
        now = datetime.datetime.utcnow()
        time = now + datetime.timedelta(hours=hours, minutes=minutes)
        pin = dict(id=str(now), time=self.toIso(time), reminders=[], actions=[])
        
        layout = generic_layout.copy()        
        pin.update({"layout":layout})
        pin["layout"]["title"] = title
        
        if subtitle:
            pin["layout"]["subtitle"] = subtitle
            
        if body:
            pin["layout"]["body"] = body
        
        self.user_token = user_token
        self.pin = pin
        self.time = time
    
    def addNotification(self, title, body=None):
        notification = generic_notification.copy()
        notification["layout"]["title"] = title
        
        if body:
            notification["layout"]["body"] = body
        
        self.pin.update({"createNotification":notification})
        
    def addReminder(self, title, hours=0, minutes=0):
        reminder = generic_reminder.copy()
        time = self.time - datetime.timedelta(hours=hours, minutes=minutes)
        reminder["time"] = self.toIso(time)
        reminder["layout"]["title"] = title
        self.pin["reminders"].append(copy.deepcopy(reminder))
    
    def addAction(self, title, url="http://192.168.2.97:5000", json={}, success="HTTP OK"):
        action = generic_action.copy()
        action["title"] = title
        action["url"] = url
        action["bodyJSON"] = json
        action["successText"] = success
        self.pin["actions"].append(copy.deepcopy(action))
          
    def toIso(self, time):
        return time.isoformat()+"Z"
        
    def send(self, skip_validation=True):
        timeline.send_user_pin(
            user_token=self.user_token,
            pin=self.pin,
            skip_validation=skip_validation
        )
    
    def display(self):
        pprint.pprint(self.pin)
    
if __name__=="__main__":
    pin1 = PinCreator("LED", minutes=5)
    pin1.addNotification("Notification")
    #pin1.addReminder("1", minutes=1)
    #pin1.addReminder("2", minutes=2)
    pin1.addAction("ON", json={"state":"LED ON"})
    pin1.addAction("OFF", json={"state":"LED OFF"})
    pin1.display()
    pin1.send()
        
