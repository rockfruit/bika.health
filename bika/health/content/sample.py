# This file only contains indexes for health
from bika.lims.interfaces import ISample
from bika.lims.interfaces import IBikaCatalog
from plone.indexer.decorator import indexer


@indexer(ISample, IBikaCatalog)
def getPatientUIDs(instance):
    uids = []
    ars = instance.getAnalysisRequests()
    for ar in ars:
        patient = ar.getField('Patient').get(ar)
        if patient:
            uids.append(patient.UID())
    return uids
