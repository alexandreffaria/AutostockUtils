import argparse
import os
import sys

def parse_arguments() -> str:
    parser = argparse.ArgumentParser(description="Image Viewer")
    parser.add_argument('folder', type=str, help='Path to the folder containing images')
    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print("The specified folder does not exist.")
        sys.exit(1)

    return args.folder