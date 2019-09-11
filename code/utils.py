from matplotlib.font_manager import FontProperties


def create_font_setting(sizes=(14, 12, 8)):
    """
    Create font axis for matplotlib and seaborn plots.
    Returns:
        (FontProperties) for title, for axis, and for ticks
    """
    title_font = FontProperties(family="Arial", size=sizes[0],
                                weight="semibold")
    axis_font = FontProperties(family="Arial", size=sizes[1])
    ticks_font = FontProperties(family="Arial", size=sizes[2])

    return title_font, axis_font, ticks_font
