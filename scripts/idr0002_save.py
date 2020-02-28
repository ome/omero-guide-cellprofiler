#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# Copyright (c) 2020 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# FPBioimage was originally published in
# <https://www.nature.com/nphoton/journal/v11/n2/full/nphoton.2016.273.html>.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Version: 1.0
#
import os
import tempfile
import warnings

from getpass import getpass

# Import OMERO Python BlitzGateway
from omero.gateway import BlitzGateway

# Import Cell Profiler Dependencies
import cellprofiler.preferences as cpprefs
import cellprofiler.pipeline as cpp

# Important to set when running headless
cpprefs.set_headless()  # noqa

# module used to inject OMERO image planes into Cell Profiler Pipeline
from cellprofiler.modules.injectimage import InjectImage


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
        files.append(path)
    print("analysis done")
    return files


# Save-results
def save_results(conn, files, plate):
    # Upload the CSV files
    print("saving results...")
    namespace = "cellprofiler.demo.namespace"
    for f in files:
        ann = conn.createFileAnnfromLocalFile(f, mimetype="text/csv",
                                              ns=namespace, desc=None)
        plate.linkAnnotation(ann)


# Disconnect
def disconnect(conn):
    conn.close()


# main
def main():
    # Collect user credentials
    username = raw_input("Username: ")
    password = getpass("OMERO Password: ")
    plate_id = raw_input("Plate ID: ")
    host = 'wss://workshop.openmicroscopy.org/omero-ws'
    # Connect to the server
    conn = connect(host, username, password)

    # Read the pipeline
    pipeline_path = "../notebooks/pipelines/ExamplePercentPositive.cppipe"
    pipeline = load_pipeline(pipeline_path)

    # Load the plate
    plate = conn.getObject("Plate", plate_id)

    files = analyze(plate, pipeline)

    save_results(conn, files, plate)
    disconnect(conn)
    print("done")


if __name__ == "__main__":
    main()
