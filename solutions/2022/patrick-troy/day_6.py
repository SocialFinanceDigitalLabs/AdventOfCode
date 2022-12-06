from aocd import get_data

session = "53616c7465645f5f932620b9dd9cb53e9facee9282730977ff26a7c28126db6fa8ce7b0" \
          "329cbec99fa54ea4d10b35d0cb2d5b3d17492e51cf4a0282caf0025e1"

datastream_buffer = get_data(day=6, year=2022, session=session).split("\n")


def marker_finder(datastream_buffer: str, packet_length: int):
    """
    Identify the location of the final character after the first unique sequence of a given packet_length

    :param datastream_buffer: string containing a list of letters
    :param packet_length: number signifying the number of unique values in a row required to identify a packet
    return integer showing the location of the final packet character
    """
    for i in range(len(datastream_buffer)):
        four_char_group = datastream_buffer[i:i+packet_length]
        if len(set(four_char_group)) == packet_length:
            marker_value = datastream_buffer.find(four_char_group)+packet_length
            return marker_value


print(marker_finder(datastream_buffer[0], packet_length=4))
print(marker_finder(datastream_buffer[0], packet_length=14))


