from mycroft import MycroftSkill, intent_file_handler

from .lib.exception import ResponseException, ConnectionException
from .lib.connector import Connector

class PiRadioControl(MycroftSkill):

    current_search = None

    def __init__(self):
        MycroftSkill.__init__(self)

    def initialize(self):
        self.connector = Connector()

    @intent_file_handler('piradio.available.intent')
    def handle_available(self):
        if self._connector.is_available():
            self.speak_dialog('piradio.available')
        else:
            self.speak_dialog('piradio.not.available')

    @intent_file_handler('piradio.channel.get.intent')
    def handle_channel_get(self, message):
        try:
            channel = self.connector.get_channel()
            self.speak_dialog('piradio.channel.get.dialog', {'channel': channel})
        except ResponseException:
            self.speak_dialog('piradio.channel.get.fail')
        except ConnectionException:
            self.speak_dialog('piradio.connection.error')

    # todo: change from file handler to parser
    @intent_file_handler('piradio.channel.set.intent')
    def handle_channel_set(self, message):
        try:
            channel = message.data.get('channel')
            if channel is not None:
                found_channels = self.connector.find_channels()
                if len(found_channels) > 5:
                    self.speak_dialog('piradio.channel.set.too.many.options')
                elif len(found_channels) > 1:
                    # ask for choices
                    channel_options = []
                    for found_channel in found_channels:
                        channel_options.append(found_channel.get('name'))

                    selected_channel = self.ask_selection(channel_options, 'piradio.channel.select.option')
                    if selected_channel is not None:
                        answer = self.connector.set_channel(message.data.channel)
                        self.speak_dialog('piradio.channel.set')
                    else:
                        self.speak_dialog('piradio.channel.set.fail')
                else:
                    self.speak_dialog('piradio.channel.unknown', {'channel': channel})
            else:
                self.speak_dialog('piradio.channel.set.fail')

        except ResponseException as x:
            self.speak_dialog('piradio.response.error')
        except ConnectionException as x:
            self.speak_dialog('piradio.offline')

    @intent_file_handler('piradio.channel.next')
    def handle_channel_next(self, message):
        try:
            channel = connector.next_channel()
            self.speak_dialog('piradio.channel.next', {'channel', channel})
        except ResponseException:
            self.speak_dialog('piradio.channel.next.failed')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    @intent_file_handler('piradio.channel.prev')
    def handle_channel_next(self, message):
        try:
            channel = connector.next_channel()
            self.speak_dialog('piradio.channel.prev', {'channel', channel})
        except ResponseException:
            self.speak_dialog('piradio.channel.prev.error')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    @intent_file_handler('piradio.volume.get.intent')
    def handle_volume_get(self, message):
        try:
            loudness = self.connector.get_volume()
            if loudness.get('mute') == True:
                self.speak_dialog('piradio.volume.muted')
            else:
                self.speak_dialog('piradio.volume.get', {'volume': loudness.get('volume')})
        except ResponseException:
            self.speak_dialog('piradio.volume.get.error')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    @intent_file_handler('piradio.volume.set.intent')
    def handle_volume_set(self, message):
        try:
            loudness = self.connector.volume_set(volume)
            self.speak_dialog('piradio.volume.set', {'volume': loudness.get('volume')})
        except ResponseException:
            self.speak_dialog('piradio.volume.set.failed')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    @intent_file_handler('piradio.volume.increase.intent')
    def handle_volume_increase(self, message):
        try:
            loudness = self.connector.volume_increase(volume)
            if self.check_answer(answer) == True:

            else:
                self.speak_dialog('piradio.volume.increase.failed')
        except ResponseException:
            self.speak_dialog('piradio.volume.increase.error')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    @intent_file_handler('piradio.volume.mute.intent')
    def handle_volume_mute(self, message):
        try:
            answer = self.connector.volume_mute()
            if self.check_answer(answer) == True:
                if 'data' in answer and 'mute' in data.answer:
                    if data.answer.mute == True:
                       self.speak_dialog('piradio.mute')
                else:
                    self.speak_dialog('piradio.mute.failed')
            else:
        except ResponseException:
            self.speak_dialog('piradio.mute.error')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    @intent_file_handler('piradio.volume.unmute.intent')
    def handle_volume_unmute(self, message):
        try:
            loudness = self.connector.volume_unmute()
            if self.check_answer(answer) == True:
                self.speak_dialog('piradio.unmute')
            else:
                self.speak_dialog('piradio.unmute.fail')
        except ResponseException:
            # try to translate error message
            self.speak_dialog('piradio.unmute.error')
        except ConnectionException
            self.speak_dialog('piradio.connection.failed')


    @intent_file_handler('piradio.song.intent')
    def handle_song_get(self, message):
        try:
            song = connector.get_song()
            if song is not None:
                self.speak_dialog('piradio.song', {"song": song})
            else:
                self.speak_dialog('piradio.song.none')
        except ResponseException:
            self.speak_dialog('piradio.song.fail')
        except ConnectionException:
            self.speak_dialog('piradio.connection.failed')

    def handle_search_track():
        # use socket connector to search via yt api
        # this search should be "cached" in order to chain with play intent
        search = self.connector.search()
        # check results
        if search

    def handle_play_track() {
        # play song on the radio via yt

        # check if song is in "cache"
        if (self.current_search is not None):
            return self.handle_play_track_from_search()

    }

    def handle_play_track_from_search():
        pass

    def handle_get_mode():
        try:
            result = self.connector.get_mode()
            mode = result.mode
        except ResponseException:
            self.speak_dialog('', {'mode': mode})
        except ConnectionException:
            self.speak_dialog('')


    def handle_set_mode():
        mode = message.data.get('mode')


    def _set_mode() {
        try:
            result = self.connector.set_mode(mode)
        except ResponseException:
            self.speak_dialog('')
        except ConnectionException:
            self.speak_dialog('')
    }

def create_skill():
    return PiRadioControl()

