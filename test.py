import argparse

def parseArgs():
    # Creating argument parser
    parser = argparse.ArgumentParser()

    # Adding arguments
    parser.add_argument("-u", "--url", help="The URL of the song or playlist to download", type=str)
    parser.add_argument("-q", "--quality", help="Set quality of downloaded song, 0 for 128 Kbps, 1 for 256 Kbps, 2 for 320 Kbps", type=int, default=0)
    parser.add_argument("-sm", "--skip-meta", help="Skip adding meta-data to songs", type=bool, default=False, nargs='?')

    # Parse args then return
    return parser.parse_args()

args = parseArgs()

for arg in args.__dict__:
    print(str(arg) + " : " + str(args.__dict__[arg]))