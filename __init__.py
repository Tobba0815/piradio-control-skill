from mycroft import MycroftSkill, intent_file_handler


class PiradioControl(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('control.piradio.intent')
    def handle_control_piradio(self, message):
        self.speak_dialog('control.piradio')


def create_skill():
    return PiradioControl()

