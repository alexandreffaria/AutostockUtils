import os
from PIL import Image, ImageFilter, ImageDraw
import sys

def apply_gaussian_blur(image):
    return image.filter(ImageFilter.GaussianBlur(radius=2))

def find_black_streaks(image):
    width, height = image.size
    top_streak_positions = []
    bottom_streak_positions = []

    # Scan from the top
    for x in range(0, width, 5):
        black_count = 0
        streak_start = None
        for y in range(height):
            if image.getpixel((x, y)) == (0, 0, 0):
                if streak_start is None:
                    streak_start = y
                black_count += 1
                if black_count >= 10:
                    top_streak_positions.append((x, streak_start))
                    break
            else:
                black_count = 0
                streak_start = None

    # Scan from the bottom
    for x in range(0, width, 5):
        black_count = 0
        streak_end = None
        for y in range(height - 1, -1, -1):
            if image.getpixel((x, y)) == (0, 0, 0):
                if streak_end is None:
                    streak_end = y
                black_count += 1
                if black_count >= 10:
                    bottom_streak_positions.append((x, streak_end))
                    break
            else:
                black_count = 0
                streak_end = None

    return top_streak_positions, bottom_streak_positions

def draw_lines(image, positions):
    draw = ImageDraw.Draw(image)
    for pos in positions:
        draw.line([(pos[0], pos[1]), (pos[0], pos[1] - 10)], fill="red", width=2)
    del draw

def process_image(file_path):
    image = Image.open(file_path)
    blurred_image = apply_gaussian_blur(image)
    top_positions, bottom_positions = find_black_streaks(blurred_image)
    draw_lines(blurred_image, top_positions)
    draw_lines(blurred_image, bottom_positions)
    blurred_image.save(file_path)  # Overwrite the original file

def main(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            file_path = os.path.join(folder_path, file_name)
            process_image(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
    else:
        folder_path = sys.argv[1]
        main(folder_path)
