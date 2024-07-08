def interpolate_colors(color_list, n):
    """
    Interpolates additional hex values between the given color_list to fill up to n colors.
    
    Parameters:
    - color_list (list): List of color hex values (strings).
    - n (int): Number of colors to return.
    
    Returns:
    - list: List of n colors interpolated between the given color_list.
    """
    if n <= 0 or len(color_list) == 0:
        return []
    
    num_colors = len(color_list)
    result_colors = []
    
    if num_colors == 1:
        # If there's only one color in the list, duplicate it n times
        return [color_list[0]] * n
    
    # Calculate how many colors to place between each pair of colors
    colors_between = (n - 1) // (num_colors - 1)
    
    for i in range(num_colors - 1):
        start_color = color_list[i]
        end_color = color_list[i + 1]
        
        for j in range(colors_between + 1):
            if j == 0:
                result_colors.append(start_color)
            elif j == colors_between:
                result_colors.append(end_color)
            else:
                # Interpolate the color based on the position between start and end
                ratio = j / (colors_between + 1)
                interpolated_color = interpolate_color(start_color, end_color, ratio)
                result_colors.append(interpolated_color)
    
    return result_colors[:n]  # Trim to exactly n colors if needed

def interpolate_color(start_color, end_color, ratio):
    """
    Interpolates a color between start_color and end_color based on ratio.
    
    Parameters:
    - start_color (str): Starting color hex value.
    - end_color (str): Ending color hex value.
    - ratio (float): Ratio between 0 and 1 indicating position between start and end.
    
    Returns:
    - str: Interpolated color hex value.
    """
    start_rgb = hex_to_rgb(start_color)
    end_rgb = hex_to_rgb(end_color)
    
    # Interpolate each RGB component
    interpolated_rgb = tuple(int(start + ratio * (end - start)) for start, end in zip(start_rgb, end_rgb))
    
    # Convert back to hex color
    interpolated_color = rgb_to_hex(interpolated_rgb)
    
    return interpolated_color

def hex_to_rgb(hex_color):
    """
    Converts a hex color string to an RGB tuple.
    
    Parameters:
    - hex_color (str): Hex color string (e.g., '#RRGGBB').
    
    Returns:
    - tuple: RGB tuple (e.g., (R, G, B)).
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb_color):
    """
    Converts an RGB tuple to a hex color string.
    
    Parameters:
    - rgb_color (tuple): RGB tuple (e.g., (R, G, B)).
    
    Returns:
    - str: Hex color string (e.g., '#RRGGBB').
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)