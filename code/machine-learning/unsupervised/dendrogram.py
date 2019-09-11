import sys

sys.path.append("../../")

from palette import Palette
from utils import create_font_setting
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

    :param ax:
    :param dist:
    :param cut:
    :param labels:
    :param leaf_rotation:
    :param leaf_font_size:
    :param sorting:
    :return:
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
    ax.legend([Line2D([0], [0], color=c, lw=6) for c in cluster_colors],
              ['Cluster %s' % i for i in range(len(cluster_colors))],
              prop=axis_font,
              loc=legend_loc, shadow=False)

    # Get color-coded clusters
    color_cluster = {col: cluster for cluster, col in enumerate(cluster_colors)}
    clusters = [[row[1]] for row in
                sorted(zip(den['leaves'],
                           [color_cluster[col] for col in
                            den['color_list'][:-2]]),
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
        ax.set_position([box.x0, box.y0, box.width*0.95, box.height])

        leg = ax.legend([Line2D([0], [0], color='white', lw=0)
                         for _ in range(len(targets)+1)],
                        [label_title.title()]+list(targets),
                        loc='center left', bbox_to_anchor=(1, 0.5),
                        prop=axis_font)
        for i, text in enumerate(leg.get_texts()[1:]):
            text.set_color(label_colors[i])
            text.set_ha('center')

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

    title, ylab, xlab = labs
    ax.set_title(title, fontproperties=title_font)
    ax.set_ylabel(ylab, fontproperties=axis_font)
    ax.set_xlabel(xlab, fontproperties=axis_font)

    return clusters


if __name__ == "__main__":
    import seaborn as sns
    from sklearn.preprocessing import StandardScaler
    from scipy.cluster.hierarchy import linkage
    import matplotlib.pyplot as plt

    # Sample 50 observations from 'mpg' dataset
    sample = sns.load_dataset('mpg').sample(50, random_state=123)
    # Set name of the model as index, and keep the first row for rows with
    # duplicate index
    sample = sample.set_index(sample.name.apply(lambda x: x.title())).iloc[:,
             :-2]
    sample = sample.loc[sample.index.drop_duplicates(keep=False)]
    # Drop rows with missing values
    sample = sample[sample.isnull().sum(axis=1) == 0]
    target = "cylinders"
    features = list(set(sample.columns) - {target})
    scaler = StandardScaler()
    sample[features] = scaler.fit_transform(sample[features])

    merging = linkage(sample[features], 'ward')
    fig, ax = plt.subplots(figsize=(13, 7.5), dpi=300)
    clusters = dendro(ax, merging, cut=7,
                      labels=sample.index,
                      root="top", leaf_rotation=90, leaf_font_size=10,
                      sorting="distance", palette_name="LaSalle",
                      cluster_colors=True, label_colors=True,
                      label_color_map=sample[target],
                      labs=(
                          "Clustering on $mpg$ Data Subsample", "Ward Distance",
                          "Car Model"))
    fig.tight_layout()
    fig.savefig("./samples/dendro_sample.png")
