from __future__ import print_function
import argparse
import chardet
import codecs
import config
import server_utils
import sys
import sbd_utils


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LUIMA Sentence Segmenter')
    parser.add_argument('-p', '--port', type=int, default=5000)
    parser.add_argument('-f', '--file')

    args = parser.parse_args(sys.argv[1:])

    if args.file:
        try:
            raw = open(args.file, 'rb').read()
            enc = chardet.detect(raw)['encoding']
            with codecs.open(args.file, mode='r', encoding=enc) as f:
                for sent in sbd_utils.text2sentences(f.read()):
                    print(sent)
                    print(config.PRINT_SEP)
        except FileNotFoundError:
            print(args.file, 'does not exist!', sep=' ')
    else:
        app = server_utils.create_app()
        app.run(port=args.port or config.DEFAULT_PORT)
