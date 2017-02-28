from bika.lims.browser.sample import SamplesView as BaseView
from Products.CMFCore.utils import getToolByName
from bika.health import bikaMessageFactory as h


class SamplesView(BaseView):

    def __init__(self, context, request):
        super(SamplesView, self).__init__(context, request)
        # Filter by patient
        self.contentFilter['getPatientUIDs'] = {
            "query": self.context.UID(), "operator": "or"}
        self.columns['Doctor'] = {'title': h('Doctor'), 'toggle': True}
        for rs in self.review_states:
            i = rs['columns'].index('getSampleID') + 1
            self.review_states[i]['columns'].insert(i, 'Doctor')

    def folderitems(self, full_objects = False):
        items = BaseView.folderitems(self, full_objects)
        if not self.workflow:
            self.workflow = getToolByName(self.context, "portal_workflow")
        outitems = []
        for x in range(len(items)):
            if 'obj' not in items[x]:
                items[x]['Doctor'] = ''
                continue
            sample = items[x]['obj']
            ars = sample.getAnalysisRequests()
            doctors = []
            doctorsanchors = []
            for ar in ars:
                doctor = ar.Schema()['Doctor'].get(ar) if ar else None
                if doctor and doctor.Title() not in doctors \
                    and self.workflow.getInfoFor(ar, 'review_state') != 'invalid':
                    doctors.append(doctor.Title())
                    doctorsanchors.append("<a href='%s'>%s</a>" % (doctor.absolute_url(), doctor.Title()))
            items[x]['Doctor'] = ', '.join(doctors);
            items[x]['replace']['Doctor'] = ', '.join(doctorsanchors)
            outitems.append(items[x])
        return outitems
