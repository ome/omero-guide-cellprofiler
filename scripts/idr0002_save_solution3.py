#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2020 University of Dundee.
#
#   Redistribution and use in source and binary forms, with or without modification, 
#   are permitted provided that the following conditions are met:
# 
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#   Redistributions in binary form must reproduce the above copyright notice, 
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
#   OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#   IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
#   INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#   HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#   OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Version: 1.0
#
import os
import tempfile
import warnings
import pandas

from getpass import getpass

# Import OMERO Python BlitzGateway
from omero.gateway import BlitzGateway
from omero.grid import DoubleColumn, ImageColumn, LongColumn, WellColumn
from omero.constants.namespaces import NSBULKANNOTATIONS
from omero.gateway import FileAnnotationWrapper
from omero.model import OriginalFileI

# Import Cell Profiler Dependencies
import cellprofiler_core.preferences as cpprefs
import cellprofiler_core.pipeline as cpp

# Important to set when running headless
cpprefs.set_headless()  # noqa

# module used to inject OMERO image planes into Cell Profiler Pipeline
from cellprofiler_core.modules.injectimage import InjectImage


# Connect to the server
def connect(hostname, username, password):
    conn = BlitzGateway(username, password,
                        host=hostname, secure=True)
    conn.connect()
    return conn


# Load-plate
def load_plate(conn, plate_id):
    return conn.getObject("Plate", plate_id)


# Load-pipeline
def load_pipeline(pipeline_path):
    pipeline = cpp.Pipeline()
    pipeline.load(pipeline_path)
    # Remove first 4 modules: Images, Metadata, NamesAndTypes, Groups...
    # (replaced by InjectImage module below)
    for i in range(4):
        print('Remove module: ', pipeline.modules()[0].module_name)
        pipeline.remove_module(1)
    print('Pipeline modules:')
    for module in pipeline.modules():
        print(module.module_num, module.module_name)
    return pipeline


# Analyze-data
def analyze(plate, pipeline):
    warnings.filterwarnings('ignore')
    print("analyzing...")
    # Set Cell Output Directory
    new_output_directory = os.path.normcase(tempfile.mkdtemp())
    cpprefs.set_default_output_directory(new_output_directory)

    files = list()
    wells = list(plate.listChildren())
    wells = wells[0:5]  # use the first 5 wells
    for count, well in enumerate(wells):
        # Load a single Image per Well
        image = well.getImage(0)
        print(image.getName())
        pixels = image.getPrimaryPixels()
        size_c = image.getSizeC()
        # For each Image in OMERO, we copy pipeline and inject image modules
        pipeline_copy = pipeline.copy()
        # Inject image for each Channel (pipeline only handles 2 channels)
        for c in range(0, size_c):
            plane = pixels.getPlane(0, c, 0)
            image_name = image.getName()
            # Name of the channel expected in the pipeline
            if c == 0:
                image_name = 'OrigBlue'
            if c == 1:
                image_name = 'OrigGreen'
            inject_image_module = InjectImage(image_name, plane)
            inject_image_module.set_module_num(1)
            pipeline_copy.add_module(inject_image_module)
        pipeline_copy.run()

        # Results obtained as CSV from Cell Profiler
        path = new_output_directory + '/Nuclei.csv'
        f = pandas.read_csv(path, index_col=None, header=0)
        f['Image'] = image.getId()
        f['Well'] = well.getId()
        f['Cell_Count'] = len(f.index)
        files.append(f)
    print("analysis done")
    return files


# Save-results
def save_results(conn, files, plate):
    # Upload the results as OMERO.table
    print("saving results...")
    Nuclei = pandas.concat(files, ignore_index=True)
    summary = Nuclei.groupby('Image').mean()
    # Free memory
    del Nuclei
    cols = []
    for col in summary.columns:
        if col == 'Image':
            cols.append(ImageColumn(col, '', summary[col]))
        elif col == 'Well':
            cols.append(WellColumn(col, '', summary[col]))
        elif summary[col].dtype == 'int64':
            cols.append(LongColumn(col, '', summary[col]))
        elif summary[col].dtype == 'float64':
            cols.append(DoubleColumn(col, '', summary[col]))
    resources = conn.c.sf.sharedResources()
    repository_id = resources.repositories().descriptions[0].getId().getValue()
    table_name = "idr0002_cellprofiler"
    table = resources.newTable(repository_id, table_name)
    table.initialize(cols)
    table.addData(cols)

    # Link the table to the plate
    orig_file = table.getOriginalFile()
    file_ann = FileAnnotationWrapper(conn)
    file_ann.setNs(NSBULKANNOTATIONS)
    file_ann._obj.file = OriginalFileI(orig_file.id.val, False)
    file_ann.save()
    plate.linkAnnotation(file_ann)
    table.close()


# Disconnect
def disconnect(conn):
    conn.close()


# main
def main():
    # Collect user credentials
    host = input("Host [wss://workshop.openmicroscopy.org/omero-ws]: ") or 'wss://workshop.openmicroscopy.org/omero-ws'
    username = input("Username [trainer-1]: ") or 'trainer-1'
    password = getpass("Password: ")
    plate_id = input("Plate ID [102]: ") or '102'
    # Connect to the server
    conn = connect(host, username, password)

    # Read the pipeline
    pipeline_path = "../notebooks/pipelines/ExamplePercentPositive.cppipe"
    pipeline = load_pipeline(pipeline_path)

    # Load the plate
    plate = load_plate(conn, plate_id)

    files = analyze(plate, pipeline)

    save_results(conn, files, plate)
    disconnect(conn)
    print("done")


if __name__ == "__main__":
    main()
