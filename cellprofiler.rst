Analyze OMERO data using CellProfiler
=====================================

CellProfiler is a free open-source software for quantitative analysis of
biological images.

For more details, visit the `CellProfiler website <http://cellprofiler.org/>`_.

**Description**
---------------

In this document, we will demonstrate how to integrate CellProfiler and
OMERO using the CellProfiler Python API and the OMERO Python API. We
will use a Jupyter notebook to demonstrate the integration.

We will show:

-  How to adjust an existing CellProfiler pipeline so that it can be used with OMERO.

-  How load images from a Plate using the OMERO API.

-  How to run CellProfiler using its Python API.

-  How to plot the results.

-  How to save the generated results back to OMERO as OMERO.table so they can be used later on by OMERO.parade.

**Setup**
---------

CellProfiler version **3.1.8** has been installed in a Docker image.

For more details, look at:

-  https://github.com/ome/training-notebooks/blob/master/Dockerfile

-  https://github.com/ome/training-notebooks/blob/master/docker/environment-python2-cellprofiler.yml

**Resources**
-------------

We will use a CellProfiler example pipeline to analyse RNAi screening
data from the Image Data Resource (IDR).

-  Pipeline \ http://cellprofiler.org/examples/#PercentPositive

-  IDR data \ https://idr.openmicroscopy.org/webclient/?show=screen-102

-  Notebook \ https://github.com/ome/training-notebooks/blob/master/CellProfiler/idr0002.ipynb

For convenience, the IDR data have been imported into the training
OMERO.server. This is only because we cannot save results back to IDR
which is a read-only OMERO.server.

**Step-by-Step**
----------------

1.  First, open the webclient and find the Plate belonging to trainer-1 named plate1_1_013.

2.  Go to \ https://idr-analysis.openmicroscopy.org/training

3.  Look under *Notebooks > CellProfiler* for idr0002.ipynb.

    .. image:: images/cp1.png

4.  Select the first Step and click on the Run button to execute each step in turn.

5.  For the connection to OMERO, you will be asked to enter your login details when running the OMERO credentials cell.

6.  Select the plate in the webclient, find the Plate ID in the right-hand panel and copy this into the plate_id variable in the next step of the notebook.

7.  The following cell loads the example pipeline and modifies it to remove the modules that are normally used for loading images from disk.

8.  These modules are replaced by the InjectImage module, using numpy planes loaded from OMERO Images. This allows to pass data from OMERO to CellProfiler.

9.  The pipeline is run on all 2-Channel images from each Well in the 96-well plate (each Well contains one image), generating a CSV file containing rows for different objects identified in the
image and columns for various parameters measured.

10. Note that to save time during the workshop, we can run on a subset of all Wells in the plate. We run it on the first 5 wells:

.. image:: images/cp2.png

11. The generated CSV file is read into a Dataframe for each image. We add the Image ID and Well ID, as well as the total number of Objects, Cell_Count, to each Dataframe.

12. All the Dataframes are then concatenated into a single Dataframe.

13. We can visualise the data as histograms for each column with
       df.hist()

.. image:: images/cp3.png


14. Finally, the Dataframe rows are grouped by Image to give an average value per Image of each parameter (column) in the table.

15. This data is saved back to OMERO as an HDF5-based table attached to the Plate, which can be read by other clients.

16. Return to the webclient and select the Plate named plate1_1_013_previously_analysed.

17. Select a Well in the central pane and open the Tables harmonica in the General tab in the right-hand pane. This will show all the CellProfiler values for this Well.

18. In the Thumbnails dropdown menu at the top-right of the centre panel, select the Parade plugin.

19. At the top-left of the centre panel choose *Add filter... > Table* to filter Wells by the data from CellProfiler.

20. Change the filter from ImageNumber to Cell_Count (at the bottom of the list).

21. Now you can use theslider to filter Wells by Cell Count.

.. image:: images/cp4.png

