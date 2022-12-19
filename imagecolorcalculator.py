import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Function to calculate the distance between two colors
def color_distance(color1, color2):
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    return ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5


# Function to get the dominant colors in an image
def get_dominant_colors(image, color_threshold):
    # Open the image and convert it to RGB
    image = Image.open(image).convert('RGB')

    # Get the width and height of the image
    width, height = image.size

    # Initialize a dictionary to store the count of each color
    color_count = {}

    # Iterate over each pixel in the image
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b = image.getpixel((x, y))

            # Convert the RGB values to a hex string
            hex_color = '#%02x%02x%02x' % (r, g, b)

            # If the hex string is not in the dictionary, add it with a count of 1
            if hex_color not in color_count:
                color_count[hex_color] = 1
            # Otherwise, increment the count for that color
            else:
                color_count[hex_color] += 1

    # Sort the dictionary by value
    sorted_colors = sorted(color_count.items(), key=lambda item: item[1], reverse=True)

    # Calculate the total number of pixels in the image
    total_pixels = width * height

    # Convert the count of each color to a percentage
    dominant_colors = {}  # Change this to a dictionary
    for color, count in sorted_colors:
        percentage = count / total_pixels * 100
        # Check if the color is similar to any of the dominant colors
        is_similar = False
        for dominant_color in dominant_colors:
            if color_distance(color, dominant_color) < color_threshold:
                # If the color is similar, add its percentage to the dominant color
                dominant_colors[dominant_color] += percentage
                is_similar = True
                break
        # If the color is not similar to any dominant colors, add it as a new dominant color
        if not is_similar:
            dominant_colors[color] = percentage

    return dominant_colors

# Function to create the GUI
# Function to create the GUI
def create_gui():
    # Create the main window
    window = tk.Tk()
    window.title('Color Analyzer')

    # Create the label and entry for the color threshold
    tk.Label(window, text='Color threshold (use 30):').grid(row=0, column=0, sticky='W')
    threshold_entry = tk.Entry(window)
    threshold_entry.grid(row=0, column=1, sticky='W')

    # Create the label and entry for the area of the painting
    tk.Label(window, text='Area of painting (sq m):').grid(row=1, column=0, sticky='W')
    area_entry = tk.Entry(window)
    area_entry.grid(row=1, column=1, sticky='W')
    
    # Create the label and entry for the minimum percentage color needs for printing
    tk.Label(window, text='Minimum percentage color needs for existing:').grid(row=2, column=0, sticky='W')
    min_entry = tk.Entry(window)
    min_entry.grid(row=2, column=1, sticky='W')

    # Create the label and button for selecting the image file
    tk.Label(window, text='Image file:').grid(row=3, column=0, sticky='W')
    file_button = tk.Button(window, text='Choose file...', command=lambda: choose_file(threshold_entry, area_entry, min_entry))
    file_button.grid(row=3, column=1, sticky='W')

    # Create a Canvas widget to display the dominant colors
    #canvas = tk.Canvas(window, width=200, height=100)
    #canvas.grid(row=4, column=0, columnspan=2)

    # Run the main loop
    window.mainloop()

def choose_file(threshold_entry, area_entry, min_entry):
    # Open a file dialog to select the image file
    file_path = filedialog.askopenfilename()
    if file_path:
        # Get the area of the painting from the entry field
        area = float(area_entry.get())
        # Display the results
        display_results(file_path, threshold_entry, area, min_entry)

# Function to display the results
def display_results(file_path, threshold_entry, area, min_entry):
    # Get the dominant colors in the image
    dominant_colors = get_dominant_colors(file_path, float(threshold_entry.get()))

    # Calculate the square meters for each color
    color_areas = {}
    color_paint = {}
    for color, percentage in dominant_colors.items():
        color_areas[color] = area * (percentage / 100)
        color_paint[color] = color_areas[color] / 10

    # Create a new window to display the results
    results_window = tk.Toplevel()
    results_window.title('Results')

    # Add a label for each color
    row = 0
    lowerV = float(min_entry.get())
    for color, area in color_areas.items():
        if dominant_colors[color] > lowerV:
            tk.Label(results_window, text=f'{color}: {dominant_colors[color]:.2f}% ({area:.1f} m2, {color_paint[color]:.1f} liters of paint)', fg = color).grid(row=row, column=0, sticky='W')
            row += 1


# Run the GUI
create_gui()