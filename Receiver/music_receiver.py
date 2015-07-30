

def split_file(file, prefix, max_size, buffer=1024):
    """
    file: the input file
    prefix: prefix of the output files that will be created
    max_size: maximum size of each created file in bytes
    buffer: buffer size in bytes

    Returns the number of parts created.
    """
    with open(file, 'r+b') as src:
        suffix = 0
        while True:
            with open(prefix + '.%s' % suffix, 'w+b') as tgt:
                written = 0
                while written < max_size:
                    data = src.read(buffer)
                    if data:
                        tgt.write(data)
                        written += buffer
                    else:
                        return suffix
                suffix += 1


def cat_files(infiles, outfile, buffer=1024):
    """
    infiles: a list of files
    outfile: the file that will be created
    buffer: buffer size in bytes
    """
    with open(outfile, 'w+b') as tgt:
        for infile in sorted(infiles):
            with open(infile, 'r+b') as src:
                while True:
                    data = src.read(buffer)
                    if data:
                        tgt.write(data)
                    else:
                        break

split_file('Kalimba.wav', 'Kalimba_split', 10*1024*1024)
list = ['Kalimba_split.0', 'Kalimba_split.1', 'Kalimba_split.2', 'Kalimba_split.3', 'Kalimba_split.4', 'Kalimba_split.5']
cat_files(list, 'Kalimba_New.wav')
