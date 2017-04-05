# This file is part of Bika LIMS
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.

# This file contains mainly indexes for samples that health needs.

from plone.indexer.decorator import indexer
from bika.lims.interfaces import ISample
from bika.lims.interfaces import IBikaCatalogSampleListing
from bika.health.utiles.sample import getPatient


# Defining the indexes for this extension. Since this is an extension, no
# getter is created so we need to create indexes in that way.
@indexer(ISample, IBikaCatalogSampleListing)
def getPatientUID(instance):
    """
    This index/column returns the patient UID for the sample.
    :param instance: the sample to create the index.
    :type instance: ATContentType
    :returns: The patient UID as string
    """
    patient = getPatient(instance)
    if patient:
        return patient.UID()
    return ''


@indexer(ISample, IBikaCatalogSampleListing)
def getDoctorsUIDs(instance):
    """
    This index/column returns the doctors UIDs for the sample.
    :param instance: the sample to create the index.
    :type instance: ATContentType
    :returns: The doctors UIDs as string
    """
    ars = instance.getAnalysisRequests()
    doctors = []
    for ar in ars:
        doctor = ar.getField('Doctor').get(ar)
        if doctor and doctor.UID() not in doctors:
            doctors.append(doctor.UID())
    return doctors


@indexer(ISample, IBikaCatalogSampleListing)
def getPatientID(instance):
    """
    This index/column returns the patient ID for the sample.
    :param instance: the sample to create the index.
    :type instance: ATContentType
    :returns: The patient ID as string
    """
    patient = getPatient(instance)
    if patient:
        return patient.getId()
    return ''


@indexer(ISample, IBikaCatalogSampleListing)
def getDoctorsIDs(instance):
    """
    This index/column returns the doctors IDs for the sample.
    :param instance: the sample to create the index.
    :type instance: ATContentType
    :returns: The doctors IDs as string
    """
    ars = instance.getAnalysisRequests()
    doctors = []
    for ar in ars:
        doctor = ar.getField('Doctor').get(ar)
        if doctor and doctor.getId() not in doctors:
            doctors.append(doctor.getId())
    return doctors


@indexer(ISample, IBikaCatalogSampleListing)
def getPatientTitleURL(instance):
    """
    This index/column returns the patient title and URL for the sample.
    :param instance: the sample to create the index.
    :type instance: ATContentType
    :returns: a string with the patient's title and URL 'title|URL'
    """
    patient = getPatient(instance)
    if patient:
        return '|'.joint([patient.Title(), patient.absolute_url_path()])
    return ''


@indexer(ISample, IBikaCatalogSampleListing)
def getDoctorTitlesURLs(instance):
    """
    This index/column returns the doctors titles and URLs for the sample.
    :param instance: the sample to create the index.
    :type instance: ATContentType
    :returns: a string with doctors titles and URLs 'Doc1|URL1,Doc2|URL2,...'
    """
    ars = instance.getAnalysisRequests()
    doctors_ids = []
    titles_urls = []
    for ar in ars:
        doctor = ar.getField('Doctor').get(ar)
        if doctor and doctor.getId() not in doctors_ids:
            doctors.append(doctor.getId())
            titles_urls.append(
                '|'.join(doctor.Title(), doctor.absolute_url_path()))
    return ','.join(titles_urls)
