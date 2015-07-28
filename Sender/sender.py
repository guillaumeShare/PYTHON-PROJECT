#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2015.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import argparse
import kodo
import os
import socket
import sys
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007


def main():
    """Example of a sender which encodes and sends a file."""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        '--file-path',
        type=str,
        help='Path to the file which should be send.',
        default=os.path.realpath(__file__))

    parser.add_argument(
        '--ip',
        type=str,
        help='The ip to send to.',
        default=MCAST_GRP)

    parser.add_argument(
        '--port',
        type=int,
        help='The port to send to.',
        default=MCAST_PORT)

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without network use.')

    args = parser.parse_args()

    # Check file.
    if not os.path.isfile(args.file_path):
        print("{} is not a valid file.".format(args.file_path))
        sys.exit(1)

    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes

    size_file = os.path.getsize(args.file_path)
    print size_file
    symbol_size = 65000
    symbols = (size_file // symbol_size) + 1
    print symbols
    label = "Received_" + args.file_path

    print label




    # In the following we will make an encoder factory.
    # The factories are used to build actual encoder
    encoder_factory = kodo.FullVectorEncoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    encoder = encoder_factory.build()

    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    # Get the data to encode.
    f = open(os.path.expanduser(args.file_path), 'rb')
    data_in = f.read()
    f.close()

    # Assign the data buffer to the encoder so that we can
    # produce encoded symbols
    encoder.set_symbols(data_in)

    address = (args.ip, args.port)

    # Send the number of symbols to the receiver
    sock.sendto(str(symbols), address)
    sock.sendto(str(symbol_size) , address)
    # Send the file name to the receiver
    sock.sendto(label , address)

    print("Processing")
    while True and not args.dry_run:
        time.sleep(0.2)
        # Generate an encoded packet
        packet = encoder.write_payload()
        print("Packet encoded!")

        # Send the packet.
        sock.sendto(packet, address)

    print("Processing finished")

if __name__ == "__main__":
    main()
