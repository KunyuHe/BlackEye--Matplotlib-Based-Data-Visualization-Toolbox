from utils import create_font_setting

def labelTitleAxis(ax, labs, font_size, fig=None):
    """
    :param ax:
    :param labs:
    :param font_size:
    :param fig:
    :return:
    """
    title, ylab, xlab = labs
    title_font, axis_font, _ = create_font_setting(font_size)

    # Axis-labels
    ax.set_ylabel(ylab, fontproperties=axis_font)
    ax.set_xlabel(xlab, fontproperties=axis_font)

    # Title
    if fig is None:
        ax.set_title(title, fontproperties=title_font)
        return ax

    st = fig.suptitle(title, fontproperties=title_font)
    st.set_y(0.975)
    fig.subplots_adjust(top=0.95)
    return fig
