"""Import the Communicate class to read uart messages.

It is designed to be used alongside the uart_microbit file."""

import serial

class Communicate:
    """Used for receiving data via uart.

    Use the read_message function to receive transmissions.

    ----------------------- Expected Message Format -------------------------

    It is expecting the messages it receives to be strings containing dictionaries, that will always have the type key.
    The other keys are defined by the type.

    Types:
        0: Start of transmission. Will have the chunkCount key. \n
        1: Data chunks. Will have the chunkID and data key. \n
        2: End of transmission. Contains no additional keys. \n
        3: End of all transmissions. Contains no additional keys.

    Upon receiving a message it will send a "RECEIVED" transmission (for every message)
    provided that they follow the expected start  of transmission, data chunks in order, end of transmission.
    """
    def __init__(self, port):
        """
        ARGS:
            port (str): the usb port to read date from. Onn linux this is '/dev/ttyACM0',
            on windows it will be something like COM7.
        """
        self.port = serial.Serial(port, 115200)
        """The port used to receive data"""
        self.last_message = None
        """Holds the last unprocessed message received by read_message
        :type: str or None"""

        self.terminated = False
        """Used by read_messages. Indicates the end of all transmissions.
        :type: bool"""


        self.send_received_message = False
        """Used to repeatedly send a received message until set to False
        :type: bool"""
        self.data_list = []
        """The list of data strings to be returned. Used by read_message only when as_list is true.
        :type: list of str"""


    def read_message(self, as_list=False, as_file=False, file_name=None):
        """This function uses uart to read a transmission.

        Transmissions must not include "|n". \n
        One of as_list and as_file must be true. If as_file is true, file_name must be provided, 
        and transmissions will be output to a file, with a newline for each.

        This function is designed to be threaded by a public function.
        
        ARGS:
            as_list (bool): indicates that all the transmissions should be outputted as a list of strings, 
                            where each list item is one transmission.
            as_file (bool): indicates that all the transmissions should be outputted to a file.
            file_name (str or None): the filename of the output file, only required if as_file is True.

        Returns:
            (str or None): The transmitted string.
        """

        received_header = False
        received_chunks = False
        last_chunk = -1 # must be -1 as read_message looks for last_chunk +1, and that needs to initially be 0
        """Holds the chunk_ID of the last received message, meaning the message must have type 1.
        :type: int"""
        total_chunks = -1
        """The total amount of data chunks to be received in the current transmission.
        :type: int"""
        received_end = False

        data = ""
        """The currently being transmitted string.
        :type: str"""

        while not self.terminated:
            message = self.port.readline().decode().strip().replace("|n", "\n") # replace is workaround for newline errors

            if not message: # guard clause, ensures there is a message to be read
                continue

            data_dict = Communicate._eval(message)

            if data_dict['type'] == 3:  # indicates end of all transmissions, must always be checked
                self.terminated = True
                self.port.write("RECEIVED".encode())
                break

            if not received_header:
                if data_dict['type'] != 0: # guard clause, 0 indicates header
                    continue

                total_chunks = data_dict['chunkCount']
                received_header = True
                self.port.write("RECEIVED".encode())

            elif not received_chunks:
                if data_dict['type'] != 1: #guard clause, 1 indicates transmission chunks
                    continue

                if data_dict['chunkID'] != last_chunk + 1: # guard clause, checks it's the right data chunk
                    continue

                data += data_dict['data']
                last_chunk = data_dict['chunkID']
                self.port.write("RECEIVED".encode())
                if last_chunk + 1 == total_chunks:
                    received_chunks = True

            elif not received_end:
                if data_dict['type'] != 2: #guard clause, 2 indicates end of current transmission
                    continue

                if as_list:
                    self.data_list.append(data)
                elif as_file:
                    with open(file_name, 'a') as f:
                        f.write(data)
                        f.write("\n")

                received_end = True
                self.port.write("RECEIVED".encode())
                continue

            else: # one transmission has ended
                if data_dict['type'] == 0: # indicates start of new transmission
                    data = ""
                    received_header = False
                    received_chunks = False
                    last_chunk = -1  # must be -1 as read_message looks for last_chunk +1, and that needs to initially be 0
                    total_chunks = -1
                    received_end = False


    @staticmethod
    def _eval(item):
        """Converts a dict as str into a python dict

        Assumes the str is a dict, does not handle errors.

        Args:
            item (str): The item to be converted, which should be a dict converted into a str
        Returns:
            (dict): The str converted into a dict"""

        new_dict = dict()

        item = item.strip()
        item = item[1:-1] # removes braces

        stored = ""
        key = None
        single_quote_open = False
        double_quote_open = False
        curly_braces_open_count = 0 # excludes original that surrounded the main dict

        def add_kv_pair(stored):
            if stored[0] != "'" and stored[0] != '"' and stored[0] != "{":
                if "." not in stored:
                    stored = int(stored)
                else:
                    stored = float(stored)
                new_dict[key] = stored

            else:
                new_dict[key] = stored[1:-1]

        i = 0
        while i < len(item):

            # get char
            c = item[i]

            # handling strings and dicts in the dict
            if c == "'":
                single_quote_open = not single_quote_open
            elif c == '"':
                double_quote_open = not double_quote_open
            elif c == "{" and not (single_quote_open or double_quote_open):
                curly_braces_open_count += 1
            elif c == "}" and not (single_quote_open or double_quote_open):
                curly_braces_open_count -= 1


            # handling the main dict
            elif c == ":" and curly_braces_open_count == 0 and not (single_quote_open or double_quote_open):
                key = stored[1:-1] # removes additional quotation marks
                stored = ""
                i += 2 # skip the following whitespace
                continue
            elif c == "," and curly_braces_open_count == 0 and not (single_quote_open or double_quote_open):
                add_kv_pair(stored)
                stored = ""
                i += 2 # skip the following whitespace
                continue


            stored += c
            i += 1

        # checks for case where final value doesn't end with ,
        if key not in new_dict:
            add_kv_pair(stored)

        return new_dict

