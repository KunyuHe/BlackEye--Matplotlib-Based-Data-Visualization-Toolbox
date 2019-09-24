import sys

sys.path.append("../../")

from palette import Palette
from utils import create_font_setting
from data import get_mpg
from title_axislabels import labelTitleAxis
from scipy.cluster.hierarchy import dendrogram, set_link_color_palette
from matplotlib.lines import Line2D


def dendro(ax, dist, cut=None,
           labels=None,
           root="top", leaf_rotation=90, leaf_font_size=10,
           sorting="distance", palette_name="LaSalle",
           cluster_colors=True, legend_loc="upper right",
           label_colors=False, label_color_map=None, label_title="",
           labs=("", "", "Distance"), font_size=(16, 12, 10)):
    """
    Plot a dendrogram given the artist and the distance matrix at minimum. Can
    produce a refined dendrogram with customized color palette for the clusters,
    and each xtick labelled (even colored if there is a target variable). Also
    enables adding legend for each cluster and the color codes if applicable.

    Inputs:
        - ax (Axes): canvas
        - dist (ndArray): the hierarchical clustering encoded as a linkage
            matrix
        - cut (float): height at which to cut the tree
        - labels (Pandas.Index): index to use for xtick labels
        - root (str): plots the root at the top with "top", and left with "left"
        - leaf_rotation (float): the angle (in degrees) to rotate the leaf
            labels
        - leaf_font_size (float): the font size (in points) of the leaf labels
        - sorting (str): for each node n, the order (visually, from
            left-to-right) n’s two descendent links are plotted is determined
            either by number of objects in its cluster descending, or by
            distance between its direct descendents descending
        - palette_name (str): user-defined palette name for 'Palette' class,
            find more in the 'palette' module
        - cluster_colors (bool): whether to use default or user-defined clusters
            coloring palette
        - legend_loc (str): location for the cluster legend, consistent with
            Matplotlib legend location definitions
        - label_colors (bool): if there is a established target variable,
            whether to color xtick labels according to that variable
        - label_color_map (Pandas.Series): target column if there is an
            established target variable (supervised)
        - label_title (str): title of the label coloring legend, using target
            column name is recommended
        - labs ((str, str, str)): title, x-axis label, y-axis label
        - font_size ((int, int, int)): title, axis label, tick label font
            properties

    Returns:
        ([[int]]) cluster output as color-coded by the dendrogram
    """
    palette = Palette().getPallete(palette_name, path="../../../palettes/")
    title_font, axis_font, ticks_font = create_font_setting(font_size)
    if cluster_colors:
        set_link_color_palette(palette.color_lst[::-1])

    default = {"show_leaf_counts": True,
               "above_threshold_color": "grey"}

    # Sort child nodes by distance or by count descending, or neither
    if sorting == "distance":
        default["distance_sort"] = 'descending'
    elif sorting == "count":
        default["count_sort"] = 'descending'

    # Plotting dendrogram and cut
    den = dendrogram(dist,
                     labels=labels,
                     orientation=root,
                     color_threshold=cut,
                     leaf_rotation=leaf_rotation, leaf_font_size=leaf_font_size,
                     **default)

    # Cluster legend
    cluster_colors = []
    for color in den['color_list']:
        if color != "grey" and color not in cluster_colors:
            cluster_colors.append(color)
    c_leg = ax.legend([Line2D([0], [0], color=c, lw=6) for c in cluster_colors],
                      ['Cluster %s' % i for i in range(len(cluster_colors))],
                      prop=axis_font,
                      loc=legend_loc, shadow=False)

    # Get color-coded clusters
    color_cluster = {col: cluster for cluster, col in enumerate(cluster_colors)}
    col_lst = den['color_list'][:] + [den['color_list'][-1]]
    for i, col in enumerate(col_lst):
        if col == "grey":
            col_lst[i] = col_lst[i-1]
    clusters = [[row[1]] for row in
                sorted(zip(den['leaves'],
                           [color_cluster[col] for col in col_lst]),
                       key=lambda x: x[0])]

    # Color the labels by target if applicable
    if label_colors:
        targets = label_color_map.unique()
        if len(targets) == 2:
            label_colors = palette.pair
        else:
            label_colors = palette.color_lst
        label_color_dict = {label: label_colors[i]
                            for i, label in enumerate(targets)}
        for lbl in ax.get_xmajorticklabels():
            lbl.set_color(label_color_dict[label_color_map[lbl.get_text()]])
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width*0.8, box.height])

        leg = ax.legend([Line2D([0], [0], color='white', lw=0)
                         for _ in range(len(targets)+1)],
                        [label_title.title()]+list(targets),
                        loc='center left', bbox_to_anchor=(1, 0.5),
                        prop=axis_font)
        for i, text in enumerate(leg.get_texts()[1:]):
            text.set_color(label_colors[i])
            text.set_ha('left')
        ax.add_artist(c_leg)

    # Plot cut
    if cut:
        if root == "left":
            func = ax.axvline
        else:
            func = ax.axhline
        func(cut, ls='--', color='r')

    ax.set_xticklabels(ax.get_xticklabels(), fontproperties=ticks_font)
    ax.set_yticklabels(ax.get_yticks(), fontproperties=ticks_font)
    ax.tick_params(axis='y', direction='in')

    labelTitleAxis(ax, labs, font_size)

    return clusters


if __name__ == "__main__":
    import seaborn as sns
    from sklearn.preprocessing import StandardScaler
    from scipy.cluster.hierarchy import linkage
    import matplotlib.pyplot as plt

    # Sample 50 observations from 'mpg' dataset
    target_name = "cylinders"
    features, target = get_mpg(target=target_name)
    merging = linkage(features, 'ward')

    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
    clusters = dendro(ax, merging, cut=7,
                      labels=features.index,
                      root="top", leaf_rotation=90, leaf_font_size=10,
                      sorting="distance", palette_name="LaSalle",
                      cluster_colors=True, label_colors=True,
                      label_color_map=target, label_title=target_name,
                      labs=(
                          "Clustering on $mpg$ Data Subsample", "Ward Distance",
                          "Car Model"))
    fig.tight_layout(rect=[0, 0, 0.9, 1])
    fig.savefig("./samples/dendro_sample.png")
