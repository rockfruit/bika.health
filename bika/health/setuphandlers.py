""" Bika setup handlers. """

from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory
from bika.lims import bikaMessageFactory as _b
from bika.health import bikaMessageFactory as _
from bika.health import logger
from bika.health.config import *
from bika.health.permissions import *
from bika.lims.interfaces import IHaveNoBreadCrumbs
from zope.event import notify
from zope.interface import alsoProvides
from Products.CMFEditions.Permissions import ApplyVersionControl
from Products.CMFEditions.Permissions import SaveNewVersion
from Products.CMFEditions.Permissions import AccessPreviousVersions


class Empty:
    pass


def setupVarious(context):
    """ Setup Bika site structure """

    if context.readDataFile('bika.health_various.txt') is None:
        return
    portal = context.getSite()

    # index objects - importing through GenericSetup doesn't
    for obj_id in (
                   'doctors',
                   'patients',
                   ):
        obj = portal._getOb(obj_id)
        obj.unmarkCreationFlag()
        obj.reindexObject()

    # same for objects in bika_setup
    bika_setup = portal._getOb('bika_setup')
    for obj_id in (
                   'bika_aetiologicagents',
                   'bika_analysiscategories',
                   'bika_drugs',
                   'bika_drugprohibitions',
                   'bika_diseases',
                   'bika_treatments',
                   'bika_immunizations',
                   'bika_vaccinationcenters',
                   'bika_casestatuses',
                   'bika_caseoutcomes',
                   'bika_epidemiologicalyears',
                   'bika_identifiertypes'
                   ):
        obj = bika_setup._getOb(obj_id)
        obj.unmarkCreationFlag()
        obj.reindexObject()

    # Move doctors and patients above Samples in nav
    portal.moveObjectToPosition('doctors', portal.objectIds().index('samples'))
    portal.moveObjectToPosition('patients', portal.objectIds().index('samples'))
    portal.moveObjectToPosition('batches', portal.objectIds().index('samples'))

    # Plone's jQuery gets clobbered when jsregistry is loaded.
    setup = portal.portal_setup
    setup.runImportStepFromProfile('profile-plone.app.jquery:default', 'jsregistry')
    setup.runImportStepFromProfile('profile-plone.app.jquerytools:default', 'jsregistry')


def setupGroupsAndRoles(context):

    if context.readDataFile('bika.health_various.txt') is None:
        return
    portal = context.getSite()

    # add roles
    for role in (
                 'Doctor',
                 ):
        if role not in portal.acl_users.portal_role_manager.listRoleIds():
            portal.acl_users.portal_role_manager.addRole(role)
        portal._addRole(role)

    # Create groups
    portal_groups = portal.portal_groups

    if 'Doctors' not in portal_groups.listGroupIds():
        portal_groups.addGroup('Doctors', title="Doctors",
            roles=['Member', 'Doctor'])

    # if 'VaccinationCenters' not in portal_groups.listGroupIds():
    #     portal_groups.addGroup('VaccinationCenters', title="",
    #         roles=['Member', ])


def setupPermissions(context):
    """ Set up some suggested role to permission mappings.
    New types and anything that differs from bika.lims gets specified here.
    These lines completely overwrite those in bika.lims - Changes common to
    both packages should be made in both places!
    """

    if context.readDataFile('bika.health_various.txt') is None:
        return
    portal = context.getSite()

    # Root permissions
    mp = portal.manage_permission
    mp(AddAnalysisRequest, ['Manager', 'Owner', 'LabManager', 'LabClerk', 'Doctor', 'Sampler'], 1)
    mp(AddSample, ['Manager', 'Owner', 'LabManager', 'LabClerk', 'Doctor', 'Sampler'], 1)
    mp(AddSamplePartition, ['Manager', 'Owner', 'LabManager', 'LabClerk', 'Doctor', 'Sampler'], 1)
    mp(AddDoctor, ['Manager', 'Owner', 'LabManager', 'LabClerk'], 1)
    mp(AddPatient, ['Manager', 'Owner', 'LabManager', 'LabClerk'], 1)

    mp(ApplyVersionControl, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Analyst', 'Owner', 'RegulatoryInspector'], 1)
    mp(SaveNewVersion, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Analyst', 'Owner', 'RegulatoryInspector'], 1)
    mp(AccessPreviousVersions, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Analyst', 'Owner', 'RegulatoryInspector'], 1)

    mp(ManageAnalysisRequests, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Analyst', 'Sampler', 'Preserver', 'Owner', 'RegulatoryInspector'], 1)
    mp(ManageDoctors, ['Manager', 'LabManager', 'Owner', 'LabClerk'], 1)
    mp(ManagePatients, ['Manager', 'LabManager', 'Owner', 'LabClerk', 'Doctor', 'RegulatoryInspector'], 1)
    portal.bika_setup.laboratory.reindexObject()

    # /clients folder permissions
    # Member role must have view permission on /clients, to see the list.
    # This means within a client, perms granted on Member role are available
    # in clients not our own, allowing sideways entry if we're not careful.
    mp = portal.clients.manage_permission
    mp(permissions.ListFolderContents, ['Manager', 'LabManager', 'Member', 'LabClerk', 'Doctor', 'Analyst', 'Sampler', 'Preserver'], 0)
    mp(permissions.View, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Member', 'Analyst', 'Sampler', 'Preserver'], 0)
    mp('Access contents information', ['Manager', 'LabManager', 'Member', 'LabClerk', 'Doctor', 'Analyst', 'Sampler', 'Preserver', 'Owner'], 0)
    portal.clients.reindexObject()

    # /doctors
    mp = portal.doctors.manage_permission
    mp(CancelAndReinstate, ['Manager', 'LabManager', 'LabClerk'], 0)
    mp('Access contents information', ['Manager', 'LabManager', 'Member', 'LabClerk', 'Doctor', 'Analyst', 'Sampler', 'Preserver', 'Owner'], 0)
    mp(permissions.ListFolderContents, ['Manager', 'LabManager', 'LabClerk', 'LabTechnician', 'Doctor', 'Owner', 'Sampler', 'Preserver'], 0)
    mp(permissions.View, ['Manager', 'LabManager', 'LabClerk', 'LabTechnician', 'Doctor', 'Owner', 'Sampler', 'Preserver'], 0)
    portal.doctors.reindexObject()

    # /patients
    mp = portal.patients.manage_permission
    mp(CancelAndReinstate, ['Manager', 'LabManager', 'Doctor', ], 0)
    mp('Access contents information', ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Sampler', 'Preserver', 'Owner', 'RegulatoryInspector'], 0)
    mp(permissions.ListFolderContents, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Owner', 'Sampler', 'Preserver', 'RegulatoryInspector'], 0)
    mp(permissions.View, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Owner', 'Sampler', 'Preserver', 'RegulatoryInspector'], 0)
    portal.patients.reindexObject()

    # /reports folder permissions
    mp = portal.reports.manage_permission
    mp(permissions.ListFolderContents, ['Manager', 'LabManager', 'Member', 'LabClerk', 'Doctor'], 0)
    mp(permissions.View, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Member'], 0)
    mp('Access contents information', ['Manager', 'LabManager', 'Member', 'LabClerk', 'Doctor', 'Owner'], 0)
    mp(permissions.AddPortalContent, ['Manager', 'LabManager', 'LabClerk', 'Doctor', 'Owner', 'Member'], 0)
    mp('ATContentTypes: Add Image', ['Manager', 'Labmanager', 'LabClerk', 'Doctor', 'Member', ], 0)
    mp('ATContentTypes: Add File', ['Manager', 'Labmanager', 'LabClerk', 'Doctor', 'Member', ], 0)
    portal.reports.reindexObject()


def setupCatalogs(context):
    # an item should belong to only one catalog.
    # that way looking it up means first looking up *the* catalog
    # in which it is indexed, as well as making it cheaper to index.

    if context.readDataFile('bika.health_various.txt') is None:
        return
    portal = context.getSite()

    def addIndex(cat, *args):
        try:
            cat.addIndex(*args)
        except:
            pass

    def addColumn(cat, col):
        try:
            cat.addColumn(col)
        except:
            pass

    # create lexicon
    wordSplitter = Empty()
    wordSplitter.group = 'Word Splitter'
    wordSplitter.name = 'Unicode Whitespace splitter'
    caseNormalizer = Empty()
    caseNormalizer.group = 'Case Normalizer'
    caseNormalizer.name = 'Unicode Case Normalizer'
    stopWords = Empty()
    stopWords.group = 'Stop Words'
    stopWords.name = 'Remove listed and single char words'
    elem = [wordSplitter, caseNormalizer, stopWords]
    zc_extras = Empty()
    zc_extras.index_type = 'Okapi BM25 Rank'
    zc_extras.lexicon_id = 'Lexicon'

    # bika_catalog
    bc = getToolByName(portal, 'bika_catalog', None)
    if bc == None:
        logger.warning('Could not find the bika_catalog tool.')
        return
    addIndex(bc, 'getPatientID', 'FieldIndex')
    addIndex(bc, 'getPatientUID', 'FieldIndex')
    addIndex(bc, 'getDoctorID', 'FieldIndex')
    addIndex(bc, 'getDoctorUID', 'FieldIndex')

    # portal_catalog
    pc = getToolByName(portal, 'portal_catalog', None)
    if pc == None:
        logger.warning('Could not find the portal_catalog tool.')
        return
    addIndex(pc, 'getDoctorUID', 'FieldIndex')
    addIndex(pc, 'getDoctorID', 'FieldIndex')
    addIndex(pc, 'getClientUID', 'FieldIndex')
    addIndex(pc, 'getClientID', 'FieldIndex')

    # bika_setup_catalog
    bsc = getToolByName(portal, 'bika_setup_catalog', None)
    if bsc == None:
        logger.warning('Could not find the bika_setup_catalog tool.')
        return
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('Disease', ['bika_setup_catalog', ])
    at.setCatalogsByType('AetiologicAgent', ['bika_setup_catalog', ])
    at.setCatalogsByType('Treatment', ['bika_setup_catalog'])
    at.setCatalogsByType('Symptom', ['bika_setup_catalog'])
    at.setCatalogsByType('DrugProhibition', ['bika_setup_catalog'])
    at.setCatalogsByType('VaccinationCenter', ['bika_setup_catalog', ])
    at.setCatalogsByType('Immunization', ['bika_setup_catalog', ])
    at.setCatalogsByType('CaseStatus', ['bika_setup_catalog', ])
    at.setCatalogsByType('CaseOutcome', ['bika_setup_catalog', ])
    at.setCatalogsByType('EpidemiologicalYear', ['bika_setup_catalog', ])
    at.setCatalogsByType('IdentifierType', ['bika_setup_catalog', ])

    # bika_patient_catalog
    bpc = getToolByName(portal, 'bika_patient_catalog', None)
    if bpc == None:
        logger.warning('Could not find the bika_patient_catalog tool.')
        return
    bpc.manage_addProduct['ZCTextIndex'].manage_addLexicon('Lexicon', 'Lexicon', elem)
    at = getToolByName(portal, 'archetype_tool')
    at.setCatalogsByType('Patient', ['bika_patient_catalog'])
    addIndex(bpc, 'path', 'ExtendedPathIndex', ('getPhysicalPath'))
    addIndex(bpc, 'allowedRolesAndUsers', 'KeywordIndex')
    addIndex(bpc, 'UID', 'FieldIndex')
    addIndex(bpc, 'Title', 'ZCTextIndex', zc_extras)
    addIndex(bpc, 'Description', 'ZCTextIndex', zc_extras)
    addIndex(bpc, 'id', 'FieldIndex')
    addIndex(bpc, 'getId', 'FieldIndex')
    addIndex(bpc, 'Type', 'FieldIndex')
    addIndex(bpc, 'portal_type', 'FieldIndex')
    addIndex(bpc, 'created', 'DateIndex')
    addIndex(bpc, 'Creator', 'FieldIndex')
    addIndex(bpc, 'getObjPositionInParent', 'GopipIndex')
    addIndex(bpc, 'sortable_title', 'FieldIndex')
    addIndex(bpc, 'review_state', 'FieldIndex')
    addIndex(bpc, 'getPatientID', 'FieldIndex')
    addIndex(bpc, 'getPrimaryReferrerUID', 'FieldIndex')
    addColumn(bpc, 'id')
    addColumn(bpc, 'UID')
    addColumn(bpc, 'Title')
    addColumn(bpc, 'Type')
    addColumn(bpc, 'portal_type')
    addColumn(bpc, 'sortable_title')
    addColumn(bpc, 'Description')
    addColumn(bpc, 'getPatientID')
    addColumn(bpc, 'getPrimaryReferrerUID')
    addColumn(bpc, 'review_state')
