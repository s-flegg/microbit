"""Import the Communicate class to send uart messages.

It is designed to be used alongside the uart_pc file."""

from time import sleep
from microbit import uart, button_a

class Communicate:
    """Used for sending data via uart.

    Use the send function to send transmissions.

    If this object is initialised with run_once set to false,
    either the terminate function will need to be used to indicate the end of all transmissions,
    or the button_terminate function needs to be run to indicate the end of all transmissions via a button press.

    --------------------- Sent Message Format -------------------

    Sent messages will be strings containing dictionaries, and will always have the type key.
    The other keys are defined by the type.

    Types:
        0: Start of transmission. Will have the chunkCount key. \n
        1: Data chunks. Will have the chunkID and data key. \n
        2: End of transmission. Contains no additional keys. \n
        3: End of all transmissions. Contains no additional keys.

    After all messages a response "RECEIVED" is expected. If not received within 5 seconds the message will be resent.
    As such "RECEIVED" should only be sent if the message follows the expected order.
    """
    def __init__(self, run_once, button_terminate):
        """Initialises the Communicate class

        ARGS:
            run_once (bool): This dictates whether the send function will only perform one full data transfer,
                            or if it will transfer data each time it is called. If False, you will need to use the
                            terminate function once all transmissions are done.
            button_terminate (bool): If True, this will allow transmissions to be stopped by pressing the A button.
                                    If False the terminate function must be used.
        """
        uart.init(baudrate=115200)
        self.run_once = run_once
        """If true, the send function should only ever send one full transmission.
        :type: bool"""
        self.complete = False
        """Used when only one transmission is set to be done, this indicates that the transmission has happened.
        :type: bool"""

        self.button_terminate = button_terminate
        """If True, check for button presses to terminate transmissions
        :type: bool"""

    def send(self, data):
        """Sends data to a computer via uart.

        The function is expected to be called repeatedly in a loop, but will only transfer each time if the run_once
        class attribute is set to false. If set to true then this class will only ever do one data transmission.
        Note that if run_once is false, no checks are performed to ensure that each transmission is unique.

        ARGS:
            data (str): The data to be sent, of undetermined length. Must not contain the string "|n".
        """
        if self.run_once and self.complete:
            return # prevent rest of func running \ data being sent

        # workaround for newline errors
        data = data.replace("\n", "|n")

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
        for i in range(len(data_chunks)):
            message = str(
                "{" + "'type': 1, 'chunkID': {chunkID}, 'data': '{data}'".format(chunkID=i, data=data_chunks[i]) + "}\n"
            )
            self._send_with_verify(message)

        # end message
        self._send_with_verify("{'type': 2}\n")

        # handle running only once
        if self.run_once:
            self.complete = True
            self.terminate()

    def terminate(self):
        """Send the end message indicating that all transmissions are complete."""
        self._send_with_verify("{'type': 3}\n")

    def _button_terminate(self):
        """Checks if Button A is pressed and terminates the uart connection if it was.


        This function should be run in a loop."""
        if button_a.was_pressed():
            self.terminate()

    def _send_with_verify(self, data):
        """Private function to send data as provided.

        Sends data as is and waits for a "RECEIVED" response.
        If response isn't received with 500 milliseconds, data is resent.

        No checks are performed to ensure the data is in suitable format, such as being <= 128 characters long.

        ARGS:
            data (str): The data to be sent, with a max length of 128 characters.
        """
        while True:
            uart.write(data)
            sleep(100)

            received = uart.read()
            if received: # ensures there is a message to run decode on, preventing errors
                if received.decode() == "RECEIVED":
                    break

            # handle button presses
            self._button_terminate() # must be in this loop otherwise this loop can prevent this ever running
