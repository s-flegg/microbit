from time import sleep

from microbit import *

class Communicate:
    """Used for sending data via uart."""
    def __init__(self):
        uart.init(baudrate=115200)

    def send(self, data=None, filename=None):
        """Sends data to a computer via uart.

        The function is expected to be called repeatedly in a loop, but it will only do one transmission.
        Either data or filename parameters should be provided, but not both.

        --------------------- For receiving transmissions ---------------------

        Sent messages will be strings containing dictionaries, and will always have the type key.
        The other keys are defined by the type.

        Types:
            0: Start of transmission. Will have the chunkCount key. \n
            1: Data chunks. Will have the chunkID and data key. \n
            2: End of transmission. Contains no additional keys.

        After all messages a response "RECEIVED" is expected. If not received within 5 seconds the message will be resent.
        As such "RECEIVED" should only be sent if the message follows the expected order.

        ARGS:
            data (str or None): The data to be sent, of undetermined length.
            filename (str or None): The name of the file to be sent.
        """
        # split data into chunks as max len for uart transmission is 128 characters
        data_chunks = []
        chunk_len = 90 # allows for message formatting
        for i in range(len(data) // chunk_len + 1):
            data_chunks.append(
                data[
                    i * chunk_len:
                    (i + 1) * chunk_len
                ]
            )


        # send transmission
        # initial/header message
        self._send_with_verify("{" + "'type': 0, 'chunkCount': {}".format(str(len(data_chunks))) + "}\n")

        # chunks
        for i in range(1, len(data_chunks)):
            message = str(
                "{" + "'type': 1, 'chunkID': {chunkID}, 'data': '{data}'".format(chunkID=i, data=data_chunks[i]) + "}\n"
            )
            self._send_with_verify(message)

        # end message
        self._send_with_verify("{'type': 2}\n")

    def _send_with_verify(self, data):
        """To be used by send.

        Sends data as is and waits for a "RECEIVED" response.
        If response isn't received with 500 milliseconds, data is resent.

        ARGS:
            data (str): The data to be sent, with a max length of 128 characters.
        """
        while True:
            uart.write(data)
            print(data)
            sleep(500)

            received = uart.read()
            if received: # ensures there is a message to run decode on, preventing errors
                if received.decode() == "RECEIVED":
                    break





