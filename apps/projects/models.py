from django.db import models
from core.models import Thing


class Project(Thing):
    # elements (forge ?)
    # issues [Open, Closed, Cancelled]
    # slug ?
    # tools (Toolbox ?)
    # parts / supplies (Warehouse ?)
    # made_by
    # specifications (="cahier des charges") / context / historique
    pass


class Part(Thing):
    # is_shared < bool > (éditable par le groupe « parts_editors » ?)
    # forked_from < UUID >
    # rating (système de validation par les pairs ?)
    # categories ["tool", "part", etc.]
    pass
