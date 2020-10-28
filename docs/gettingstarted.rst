Getting started with CellProfiler and OMERO
===========================================

Description
-----------

We will use a Python script showing how to analyze data stored in an OMERO server
using the CellProfiler API.

We will show:

- How to connect to server.

- How load images from a Plate using the OMERO API.

- How to run CellProfiler using its Python API.

- How to save the generated results and link them to the Plate.

Resources
---------

We will use a CellProfiler example pipeline to analyse RNAi screening
data from the Image Data Resource (IDR).

- Example pipeline from the CellProfiler website: `Cell/particle counting and scoring the percentage of stained objects <http://cellprofiler-examples.s3.amazonaws.com/ExamplePercentPositive.zip>`_.


- Images from IDR `idr0002 <https://idr.openmicroscopy.org/search/?query=Name:idr0002>`_.

For convenience, the IDR data have been imported into the training
OMERO.server. This is only because we cannot save results back to IDR
which is a read-only OMERO.server.

Setup
-----

We recommend to use a Conda environment to install CellProfiler and the OMERO Python bindings. Please read first :doc:`setup`.

Step-by-Step
------------

In this section, we go over the various steps required to analyse the data.
The script used in this document is :download:`idr0002_save.py <../scripts/idr0002_save.py>`.

When running CellProfiler **headless**, it is important to set the following:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # run headless
    :end-before: # end headless


Connect to the server:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # Connect
    :end-before: # Load-plate


Load the plate:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # Load-plate
    :end-before: # Load-pipeline


A CellProfiler pipeline usually expects the files to be analyzed to be available locally.
This is not the case here. So we first need to remove some modules from the pipeline so we can then inject data retrieved from the OMERO server:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # Load-pipeline
    :end-before: # Analyze-data


We are now ready to analyze the plate:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # Analyze-data
    :end-before: # Save-results


Let's now save the generated CSV files and link them to the plate:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # Save-results
    :end-before: # Disconnect


When done, close the session:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # Disconnect
    :end-before: # main


In order to use the methods implemented above in a proper standalone script:
**Wrap it all up** in an ``analyze`` method and call it from ``main``:

.. literalinclude:: ../scripts/idr0002_save.py
    :start-after: # main

**Exercises**
-------------

#. Modify the script above to analyze images in a dataset (:download:`Solution <../scripts/idr0002_save_solution1.py>`).

#. Modify the script to link the generated results to the corresponding image (:download:`Solution <../scripts/idr0002_save_solution2.py>`).

#. Modify the script to aggregate the result in an OMERO.table and link the output to the plate (:download:`Solution <../scripts/idr0002_save_solution3.py>`).
