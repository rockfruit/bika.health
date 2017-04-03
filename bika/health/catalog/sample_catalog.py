# This file is part of Bika Health
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

from bika.lims.catalog import CATALOG_SAMPLE_LISTING

# Defines the extension for catalogs created in Bika LIMS.
# Only add the items you would like to add!
sample_catalog_definition = {
    CATALOG_SAMPLE_LISTING: {
            'indexes': {
                'getDoctorsUIDs': 'KeywordIndex',
                'getPatientUID': 'UUIDIndex',
                # To sort columns
                'getPatientID': 'FieldIndex',
                'getDoctorsIDs': 'KeywordIndex',
            },
            'columns': [
                'getPatientID',
                'getClientPatientID',
                'getPatientTitle',
                'getDoctorsTitles'
            ]
        }
    }
