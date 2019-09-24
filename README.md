# DarkEyes: Matplotlib-Based Data Visualization Toolbox
> I was given dark eyes by the dark night,    
>
> Yet I use them to search for light

Author: Kunyu He

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6c7f29194f96496983fc81aac4df4176)](https://www.codacy.com/manual/kunyuhe/DarkEyes--Matplotlib-Based-Data-Visualization-Toolbox?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KunyuHe/DarkEyes--Matplotlib-Based-Data-Visualization-Toolbox&amp;utm_campaign=Badge_Grade) [![Maintainability](https://api.codeclimate.com/v1/badges/dc621cd23291e6e5b881/maintainability)](https://codeclimate.com/github/KunyuHe/DarkEyes--Matplotlib-Based-Data-Visualization-Toolbox/maintainability) [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Motivation

Project `DarkEyes` is motivated primarily by the need of presentation-ready data visualizations in an applied data science workflow.

Data science professionals who use Python day-to-day might be good at exploratory data analysis (EDA) where plots are mostly for self-use, yet not as good at producing presentation-ready plots that are customized to certain standards or requests. It sometimes takes hours of googling to find how to change a small part of a graph, and even longer to fit the hints to their needs. This might result from the fact that most `Matplotlib` users are not familiar with the package. They use the `Pyplot` API (`plt.plot`) of `Matplotlib` all the time, and have little or no experience interacting with the object-oriented API (`ax.plot`), where users can have full control over the plotting.

`DarkEyes` is here to help. It provides a higher-level user interface that fits in a variety of use cases in EDA and machine learning to produce presentation-ready data visualizations. Users can preview the end-products from command line to see if there's a fit, and easily adapt the functions to their needs in Jupyter Notebook. The way users interact with `DarkEyes` API is by specifying certain positional arguments at minimum, and continue to specify optional ones to apply the extensions. Users that are rather familiar with the object-oriented API of `Matplotlib` can continue to work on the returned `Axes` from `DarkEyes` outputs, should they want to further customize the plots.

In short, **`DarkEyes` is a `Matplotlib`-based visualization toolbox that serves to simplify the production and help enhance the quality of presentation-ready data visualizations in EDA and machine learning processes for applied data science professionals who are not familiar with the object-oriented API of `Matplotlib`.**

## User's Guide

  

### 1. Installing



### 2. Use Cases

| Name       | Type                            | Short Description                                            | Features                                                     |
| ---------- | ------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Dendrogram | Machine Learning (Unsupervised) | Dendrogram serves to show the results of hierarchical clustering. It illustrates the arrangement of the clusters visually. | Text labels colored by target variable if applicable; Return clusters as colored |

