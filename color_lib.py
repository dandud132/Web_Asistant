from colorthief import ColorThief



import math

def rgb_to_name(r, g, b):
    # Define the basic rainbow colors in RGB format
    rainbow_colors = {
        'Red': (255, 0, 0),
        'Orange': (255, 165, 0),
        'Yellow': (255, 255, 0),
        'Green': (0, 255, 0),
        'Cyan': (0, 255, 255),
        'Blue': (0, 0, 255),
        'Violet': (238, 130, 238),
        'Black': (0, 0, 0)
    }

    # Function to calculate the Euclidean distance between colors
    def euclidean_distance(color1, color2):
        return math.sqrt((color1[0] - color2[0])**2 + (color1[1] - color2[1])**2 + (color1[2] - color2[2])**2)

    # Find the closest color
    closest_color_name = None
    min_distance = float('inf')

    for color_name, color_rgb in rainbow_colors.items():
        distance = euclidean_distance((r, g, b), color_rgb)
        if distance < min_distance:
            min_distance = distance
            closest_color_name = color_name

    return closest_color_name

def color_name (image):
    color_thief = ColorThief(image)

    palette = color_thief.get_palette(color_count=2, quality=1)

    color = palette[1]
    color_array = []
    for i in color:
        color_array.append(i)
    r, g, b = color_array[0], color_array[1], color_array[2]

    color_name = rgb_to_name(r,g,b)
    return color_name


