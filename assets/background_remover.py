from rembg import remove
from PIL import Image
import argparse

parser = argparse.ArgumentParser("background_remover.py <pic>")
parser.add_argument("pic", help="The picture where you want to remove the background from", type=str)

args = parser.parse_args()

def main():
    if args.pic:
        input = Image.open(args.pic)
    else:
        raise ValueError("No picture provided")

    output = remove(input)



    output.save("output.png")




if __name__ == "__main__":
    main()