# django-modeltranslation modifies the model.
# We ensure the new fields are present on the model before simple history builds the historical version of the model
# See: https://github.com/treyhunner/django-simple-history/issues/209

from .element import *
from .project import *
from .publication import *
from .workshop import *
