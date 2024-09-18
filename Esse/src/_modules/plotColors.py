from all_imports import *
from .plotUtils import interpolate_colors

TUMBlue = "#0065bd"
Black = "#000000"
White = "#ffffff"
DarkBlue = "#005293"
LightBlue = "#64a0c8"
LighterBlue = "#98c6ea"
Gray = "#999999"
Orange = "#e37222"
Green = "#a2ad00"
LightGray = "#dad7cb"

tum_blue_brand = "#3070B3"
tum_blue_dark = "#072140"
tum_blue_dark_1 = "#0A2D57"
tum_blue_dark_2 = "#0E396E"
tum_blue_dark_3 = "#114584"
tum_blue_dark_4 = "#14519A"
tum_blue_dark_5 = "#165DB1"
tum_blue_light = "#5E94D4"
tum_blue_light_dark = "#9ABCE4"
tum_blue_light_2 = "#C2D7EF"
tum_blue_light_3 = "#D7E4F4"
tum_blue_light_4 = "#E3EEFA"
tum_blue_light_5 = "#F0F5FA"
tum_yellow = "#FED702"
tum_yellow_dark = "#CBAB01"
tum_yellow_1 = "#FEDE34"
tum_yellow_2 = "#FEE667"
tum_yellow_3 = "#FEEE9A"
tum_yellow_4 = "#FEF6CD"
tum_orange = "#F7811E"
tum_orange_dark = "#D99208"
tum_orange_1 = "#F9BF4E"
tum_orange_2 = "#FAD080"
tum_orange_3 = "#FCE2B0"
tum_orange_4 = "#FEF4E1"
tum_pink = "#B55CA5"
tum_pink_dark = "#9B468D"
tum_pink_1 = "#C680BB"
tum_pink_2 = "#D6A4CE"
tum_pink_3 = "#E6C7E1"
tum_pink_4 = "#F6EAF4"
tum_blue_bright = "#8F81EA"
tum_blue_bright_dark = "#6955E2"
tum_blue_bright_1 = "#B6ACF1"
tum_blue_bright_2 = "#C9C2F5"
tum_blue_bright_3 = "#DCD8F9"
tum_blue_bright_4 = "#EFEDFC"
tum_red = "#EA7237"
tum_red_dark = "#D95117"
tum_red_1 = "#EF9067"
tum_red_2 = "#F3B295"
tum_red_3 = "#F6C2AC"
tum_red_4 = "#FBEADA"
tum_green = "#9FBA36"
tum_green_dark = "#7D922A"
tum_green_1 = "#B6CE55"
tum_green_2 = "#C7D97D"
tum_green_3 = "#D8E5A4"
tum_green_4 = "#E9F1CB"
tum_grey_1 = "#20252A"
tum_grey_2 = "#333A41"
tum_grey_3 = "#475058"
tum_grey_4 = "#6A757E"
tum_grey_7 = "#DDE2E6"
tum_grey_8 = "#EBECEF"
tum_grey_9 = "#FBF9FA"
tum_white = "#FFFFFF"

#https://www.learnui.design/tools/data-color-picker.html#palette

#lets define some gradients!

#based on tum_blue_dark
color_list = ['#dee0e5', '#bec1cc', '#9fa3b3', '#80879a', '#626b83', '#46516c', '#293855', '#072140']
TUMBlueDarkSingleHueScale = ListedColormap(interpolate_colors(color_list, 30))


# Thesis Colorpaeltte
cNeonpink = '#FF407D'
cPink = '#FFCAD4'
cBlue = '#40679E'
cDarkBlue = '#1B3C73'
cOrange = '#FC4100'
cYellow = '#FFC55A'
cGrey = "#6A757E" #tum_green_4
cLightblue = "#9ABCE4" #tum_blue_light_dark

color_lighthouse = '#F3F4F4'
color_citylights = '#DFE6EA'
color_coralpink = '#F88379'
color_vulcanfire = '#E6390D'
color_deepseablue = '#2A4B5A'
color_elderberryblack = '#1E323B'

color_list = [color_lighthouse, color_citylights, color_coralpink, color_vulcanfire, color_deepseablue, color_elderberryblack]
gradient_lightvulcanelderberry = ListedColormap(interpolate_colors(color_list, 30))



