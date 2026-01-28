from microbit import *

class Communicate:

    def __init__(self, run_once, button_end):
        """Initialises the Communicate class

        ARGS:
            run_once (bool): This dictates whether the send function will only perform one full data transfer,
                            or if it will transfer data each time it is called. If False, you will need to use the
                            terminate function once all transmissions are done.
            button_end (bool): If True, this will allow transmissions to be stopped by pressing the A button.
                                    If False the terminate function must be used.
        """
        uart.init(baudrate=115200)
        self.run_once = run_once
        """If true, the send function should only ever send one full transmission.
        :type: bool"""
        self.complete = False
        """Used when only one transmission is set to be done, this indicates that the transmission has happened.
        :type: bool"""

        self.button_end = button_end
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
        
        def send_with_verify(data):
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
                if button_a.was_pressed():
                    send_with_verify("{'type': 3}\n") # end all transmissions message
        
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
        send_with_verify("{" + "'type': 0, 'chunkCount': {}".format(str(len(data_chunks))) + "}\n")

        # chunks
        for i in range(len(data_chunks)):
            message = str(
                "{" + "'type': 1, 'chunkID': {chunkID}, 'data': '{data}'".format(chunkID=i, data=data_chunks[i]) + "}\n"
            )
            send_with_verify(message)

        # end message
        send_with_verify("{'type': 2}\n")

        # handle running only once
        if self.run_once:
            self.complete = True
    


