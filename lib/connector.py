import sys
import platform
import subprocess
import _thread
import time
import json
import rapidfuzz
import websocket
from exception.ConnectionException import ConnectionException
from exception.ResponseException import ResponseException

class Connector():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def is_available(self):
        # todo: remove param, since target will always be unix like
        param = '-n' if platform.system().lower()=='windows' else '-c'
        command = ['ping', param, '1', self.ip]

        return subprocess.call(command, stdout=subprocess.DEVNULL) == 0

    def get_volume(self):
        response = self._send('volume get')
        self._check_response(response)
        return self._get_values(response, [], 'volume')

    def set_volume(self, volume):
        response = self._send('volume set {}'.format(volume))
        self._check_response(response)
        return self._get_value(response, 'volume', 'volume')

    def volume_mute(self):
        response = self._send('volume mute on')
        self._check_response(response)
        return self._get_value(response, 'mute', 'volume')

    def volume_unmute(self):
        response = self._send('volume mute off')
        self._check_response(response)
        return self._get_value(response, 'mute', 'volume')

    def volume_increase(self, amount):
        if amount is not None:
            response = self._sent('volume increase {}'.format(amount))
        else:
            response = self._send('volume increase')

        self._check_response(response)
        return self._get_value(response, 'volume', 'volume')

    def volume_decrease(self, amount):
        if amount is not None:
            response = self._send('volume decrease {}'.format(amount))
        else:
            response = self._send('volume decrease')

        self._check_response(response)
        return self._get_value(response, 'volume', 'volume')

    def get_channel_list(self):
        response = self._send('radio list')
        channel_list = self._get_value(response, 'programList')
        ## return non data channels only
        return filter(lambda c: (c.get('serviceComponentID') == '00'), channel_list)

    def find_channel(self, desired_channel, min_ratio=70):
        channel_list = connector.get_channel_list()

        matching_channels = []
        for channel in channel_list:
            ratio = rapidfuzz.fuzz.partial_ratio(channel.get('name').lower(), desired_channel)
            if ratio >= min_ratio:
                matching_channels.append(channel)

        return matching_channels

    def get_channel(self):
        return self._get_value(self.get_info(), 'programName')

    def prev_channel(self):
        return self._send('radio prev')

    def next_channel(self):
        return self._send('radio next')

    def set_channel(self, channel):
        return self._send('radio play {}'.format(channel))

    def get_info(self):
        return self._send('radio info')

    def get_mode(self):
        return self.send('config get mode')

    def get_modes(self):
        return self.send('config get mode')

    def get_song(self):
        return self._get_value(self.get_info(), 'programText')

    def _check_response(self, response):
        if response is None:
            raise ResponseException('No response')
        elif not 'status' in response or not 'message' in response:
            raise ResponseException('Malformed response')
        elif 'status' in response and response.get('status') != 0:
            raise ResponseException(response.get('message'))

    def _get_value(self, response, key, category='radio'):
        #self._check_response(response)
        if 'data' in response and category in response.get('data') and key in response.get('data').get(category):
            return response.get('data').get(category).get(key)
        else:
            return None

    def _get_values(self, response, keys=[], category='radio'):
        result = {}
        if 'data' in response and category in response.get('data'):
            data = response.get('data').get(category)
            if len(keys) == 0:
                result = data
            else:
                for key in keys:
                    if key in data:
                       result.update({key: data.get(key)})
        return result

    def _connect(self, timeout=3):
        uri = 'ws://' + self.ip + ':' + str(self.port)
        # websocket.enableTrace(True)
        ws = websocket.WebSocket()
        ws.connect(uri, timeout=timeout)
        return ws

    def _send(self, command):

        answer = None
        try:
            ws = self._connect()
        except TimeoutError:
            raise ConnectionException

        ws.send(json.dumps({'type': 'request', 'command': command}))

        timeout = False
        max_time = time.time() + 3

        while True:
            maybe_answer = ws.recv()
            parsed_message = json.loads(maybe_answer)
            if command != 'radio info' and 'type' in parsed_message and parsed_message.get('type') == 'response':
                if 'command' in parsed_message and parsed_message.get('command') == command:
                    answer = parsed_message
                    break
            elif 'type' in parsed_message and parsed_message.get('type') == 'info':
                if command == 'radio info' and 'data' in parsed_message:
                    data = parsed_message.get('data')
                    if 'radio' in data and len(data.get('radio')) > 2:
                        answer = parsed_message
                        break

            if time.time() > max_time:
                timeout = True
                break

        ws.close()

        if answer is None:
            raise ResponseException(timeout=timeout)

        return answer

connector = Connector(ip='192.168.178.60', port=32323)

try:
    #print({'available': connector.is_available()})
    #print(connector.get_info())
    print(connector.get_channel())
    print(connector.get_song())
    print(connector.get_volume())
    #print(connector.volume_increase())
    #print(connector.set_volume('30'))
    print(connector.find_channel('regenbogen'))

except ConnectionException as x:
    print(x.message)
except ResponseException as x:
    print('Response Exception: ')
    print(x.message)
