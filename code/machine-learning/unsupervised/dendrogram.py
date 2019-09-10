import sys
sys.path.append("../../../")

from utils import getPallete
from scipy.cluster.hierarchy import dendrogram, set_link_color_palette

def dendro(ax, dist, cut=None,
           labels=None,
           root="top", leaf_rotation=90, leaf_font_size=10,
           sorting="distance", palette="LaSalle",
           cluster_colors=None, label_colors=None, label_color_map=None):
    """
    Plot a dendrogram given the artist and the distance matrix at minimum. Can
    produce a refined dendrogram with customized color palette for the clusters,
    and each xtick labelled (even colored if there is a target variable). Also
    enables adding legend for each cluster and the color codes if applicable.

    :param ax:
    :param dist:
    :param cut:
    :param labels:
    :param leaf_rotation:
    :param leaf_font_size:
    :param sorting:
    :return:
    """
    if cluster_colors is not None:
        palette, _ = getPallete(cluster_colors)
        set_link_color_palette(palette)

    default = {"show_leaf_counts": True,
               "above_threshold_color": "grey"}

    # Sort child nodes by distance or by count descending, or neither
    if sorting == "distance":
        default["distance_sort"] = 'descending'
    elif sorting == "count":
        default["count_sort"] = 'descending'

    dendrogram(dist,
               labels=labels,
               orientation=root,
               color_threshold=cut,
               leaf_rotation=leaf_rotation, leaf_font_size=leaf_font_size,
               **default)
    if root == "left":
        func = ax.axvline
    else:
        func = ax.axhline
    func(cut, ls='--', color=utils.RED)

    if label_colors is not None:
        for lbl in ax.get_xmajorticklabels():
            lbl.set_color(label_colors[label_color_map[lbl.get_text()]])