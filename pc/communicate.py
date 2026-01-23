import serial

class Communicate:
    def __init__(self):
        self.port = serial.Serial('COM7', 115200)

        self.received_header = False
        self.received_chunks = False
        self.last_chunk = -1 # must be -1 as read_message looks for last_chunk +1, and that needs to initially be 0
        self.total_chunks = None
        self.received_end = False

        self.data = ""

    def read_message(self):
        """This function uses uart to read a transmission once.

        It will only read the transmission once.
        It is expecting the messages it receives to be strings containing dictionaries, that will always have the type key.
        The other keys are defined by the type.

        Types:
            0: Start of transmission. Will have the chunkCount key. \n
            1: Data chunks. Will have the chunkID and data key. \n
            2: End of transmission. Contains no additional keys.

        Upon receiving a message it will send a "RECEIVED" transmission (for every message)
        provided that they follow the expected start  of transmission, data chunks in order, end of transmission.

        Returns:
            (str): The transmitted string.
        """
        while True:
            message = self.port.readline().decode().strip()

            if not message: # guard clause, ensures there is a message to be read
                continue

            data = self.eval(message)
            print(f"____DATA____: {data}")

            if not self.received_header:
                if data['type'] != 0: # guard clause, 0 indicates header
                    continue

                self.total_chunks = data['chunkCount']
                self.received_header = True
                self.port.write("RECEIVED".encode())

            elif not self.received_chunks:
                if data['type'] != 1: #guard clause, 1 indicates transmission chunks
                    continue

                if data['chunkID'] != self.last_chunk + 1: # guard clause, checks it's the right data chunk
                    continue

                self.data += data['data']
                self.last_chunk = data['chunkID']
                self.port.write("RECEIVED".encode())
                if self.last_chunk + 1 == self.total_chunks:
                    self.received_chunks = True

            elif not self.received_end:
                if data['type'] != 2: #guard clause, 2 indicates end, currently redundant but useful if more types added
                    continue

                self.received_end = True
                self.port.write("RECEIVED".encode())
                break

        return self.data

    def eval(self, item):
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


if __name__ == "__main__":
    a = Communicate()
    print(a.read_message())
    # print(a.eval("""{'test': '123', 'sbc': "8, 6, \n12", 'abc': 4.2, 'bef': {'a': 2}}"""))
    # print(a.eval(" {'type': 0, 'chunkCount': 7}"))
