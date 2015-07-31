__author__ = 'USER'
#! /usr/bin/env python
# encoding: utf-8

# Copyright Steinwurf ApS 2015.
# Distributed under the "STEINWURF RESEARCH LICENSE 1.0".
# See accompanying file LICENSE.rst or
# http://www.steinwurf.com/licensing

import argparse
import kodo
import socket
import struct
import sys
import time
import numpy as np
import cv2
import pymedia
import pymedia.audio.sound as sound
import wave

import threading


MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

##def get_music(decoder, i, sr):
##    global music_buffer
##    music_buffer = ''
##    j = i
##    while True:
##        music_buffer += decoder.copy_symbols()[(j)*(sr):(j+1)*sr]
##        j += 1
    
    

def main():
    """
    Multicast example, reciever part.

    An example where data is received, decoded, and finally written to a file.
    """
    parser = argparse.ArgumentParser(description=main.__doc__)

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

    sock = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP)

    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('', args.port))
    mreq = struct.pack("4sl", socket.inet_aton(args.ip), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Set the number of symbols (i.e. the generation size in RLNC
    # terminology) and the size of a symbol in bytes
    symbols = int(sock.recv(100))
    print symbols
    symbol_size = int(sock.recv(100))
    print symbol_size

    # Get the filename from the sender
    file_name = sock.recv(100)
    print file_name
    sampleRate = int(sock.recv(100))
    # In the following we will make an decoder factory.
    # The factories are used to build actual decoder
    decoder_factory = kodo.FullVectorDecoderFactoryBinary(
        max_symbols=symbols,
        max_symbol_size=symbol_size)

    decoder = decoder_factory.build()

    print "SampleRate {}".format(sampleRate)
    snd1= sound.Output(sampleRate, 2, sound.AFMT_S16_LE )

    rating = int(sampleRate*1.02)
    if args.dry_run:
        sys.exit(0)

    print("Processing...")
    i = 0

    #t = threading.Thread(target=get_music, args=(decoder, i, sampleRate, ))
    
    while not decoder.is_complete():
        time.sleep(0.1)
        packet = sock.recv(rating)

        decoder.read_payload(packet)
        #music_buffer += decoder.copy_symbols()[(i)*(sampleRate):(i+1)*sampleRate]      
##          if i == 0:
##                    t.start()
##                
        if i >= 10:
            snd1.play(decoder.copy_symbols()[(i-10)*(rating):(i-10)*rating + rating])
        #print len(decoder.copy_symbols())
        #snd1.play(decoder.copy_symbols())
        #while snd1.isPlaying():
            #time.sleep(0.05)

        #print("Packet received!")
        print("Decoder rank: {}/{}".format(decoder.rank(), decoder.symbols()))
        i += 1

    # Write the decoded data to the output file
    f = open(file_name, 'wb')
    f.write(decoder.copy_symbols())
    f.close()
    #music_buffer.close()
    print("Processing finished.")

if __name__ == "__main__":
    main()
