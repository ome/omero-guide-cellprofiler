Install CellProfiler
====================

In this section, we indicate how to install CellProfiler in a `Conda <https://conda.io/en/latest/>`_ environment.
We will use the CellProfiler API to analyze data stored in an OMERO server.

CellProfiler currently runs on Python 2.7. It does not yet support Python 3.


**Setup**
---------

We recommand to install CellProfiler using Conda.
Conda manages programming environments in a manner similar to 
`virtualenv <https://virtualenv.pypa.io/en/stable/>`_.

- We assume that you have a local copy of the `omero-guide-cellprofiler repository <https://github.com/ome/omero-guide-cellprofiler>`_. If not, first clone the repository::

    $ git clone https://github.com/ome/omero-guide-cellprofiler.git

- Install `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ if necessary.

- Create a programming environment using Conda::

    $ conda create -n cellprofiler python=2.7

- Install CellProfiler **3.1.9** and its dependencies using an installation file::

    $ conda env update -n cellprofiler --file binder/environment.yml 

