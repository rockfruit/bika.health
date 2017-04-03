# This file is part of Bika LIMS
#
# Copyright 2011-2016 by it's authors.
# Some rights reserved. See LICENSE.txt, AUTHORS.txt.
from Products.CMFCore.utils import getToolByName
from bika.health import logger


def getPatient(sample):
    """
    This function returns the patient object associated with the sample.

    :param sample: The sample object
    :type sample: ATContentType
    :returns: the patient object or None
    :rtype: ATContentType/None
    """
    # Onse sample can have more than one AR associated, but if is
    # the case, we must only take into account the one that is not
    # invalidated/retracted
    rawars = sample.getAnalysisRequests()
    ars = [ar for ar in rawars
           if (ar.review_state != 'invalid')]
    if (len(ars) == 0 and len(rawars) > 0):
        # All ars are invalid. Retrieve the info from the last one
        ar = rawars[len(rawars) - 1]
    elif (len(ars) > 1):
        # There's more than one valid AR
        # That couldn't happen never. Anyway, retrieve the last one
        ar = ars[len(ars) - 1]
    elif (len(ars) == 1):
        # One ar matches
        ar = ars[0]
    if not ar:
        logger.error(
            "Analysis request with ID '{}' doesn't have a sample."
            .format(sample.id))
        return None
    field = ar.getField('Patient')
    return field.get(ar) if field else None
