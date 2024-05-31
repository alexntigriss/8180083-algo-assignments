import sys
import math
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("algorithm", choices=["viterbi", "trellis"])
    parser.add_argument("file_path")
    parser.add_argument("-s", "--scale", type=float, default=3)
    parser.add_argument("-g", "--penalty", type=float, default=0.5)
    parser.add_argument("-d", "--debug", action="store_true")
    args = parser.parse_args()
    
    print(args)

if __name__ == "__main__":
    main()