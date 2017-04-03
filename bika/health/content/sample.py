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
# TODO-catalog: delete this index
@indexer(ISample, IBikaCatalogSampleListing)
def getPatientUID(instance):
    patient = getPatient(instance)
    if patient:
        return patient.UID()
    return ''


@indexer(ISample, IBikaCatalogSampleListing)
def getDoctorsUIDs(instance):
    ars = instance.getAnalysisRequests()
    doctors = []
    for ar in ars:
        doctor = ar.getField('Doctor').get(ar)
        if doctor and doctor.UID() not in doctors:
            doctors.append(doctor.UID())
    return doctors


@indexer(ISample, IBikaCatalogSampleListing)
def getPatientID(instance):
    patient = getPatient(instance)
    if patient:
        return patient.getId()
    return ''


@indexer(ISample, IBikaCatalogSampleListing)
def getDoctorsIDs(instance):
    ars = instance.getAnalysisRequests()
    doctors = []
    for ar in ars:
        doctor = ar.getField('Doctor').get(ar)
        if doctor and doctor.getId() not in doctors:
            doctors.append(doctor.getId())
    return doctors


@indexer(ISample, IBikaCatalogSampleListing)
def getPatientTitle(instance):
    return ''


@indexer(ISample, IBikaCatalogSampleListing)
def getDoctorTitles(instance):
    return ''
