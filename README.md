# Guide on how to integrate CellProfiler and OMERO
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ome/omero-guide-cellprofiler/master?filepath=notebooks/idr0002.ipynb)

This guide demonstrates how to use the CellProfiler Python API to analyze data stored in [IDR](https://idr.openmicroscopy.org/) or in another OMERO server.

This repository contains documentation and notebooks.

To run the notebooks, you can either [run on mybinder.org](https://mybinder.org/v2/gh/ome/omero-guide-cellprofiler/master?filepath=notebooks) or build locally with [repo2docker](https://repo2docker.readthedocs.io/).


To build locally:

 * Install [Docker][https://www.docker.com/] if required
 * Create a virtual environment and install repo2docker from PyPI.
 * Clone this repository
 * Run  ``repo2docker``. 
 * Depending on the permissions, you might have to run the command as an admin

```
pip install jupyter-repo2docker
git clone https://github.com/ome/omero-guide-cellprofiler.git
cd omero-guide-cellprofiler
repo2docker .
```


This a Sphinx based documentation. 
If you are unfamiliar with Sphinx, we recommend that you first read 
[Getting Started with Sphinx](https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html).
