import simple_history
from core.models import ProjectType, Project
from modeltranslation.translator import translator, TranslationOptions


class ProjectTypeTranslationOptions(TranslationOptions):
    fields = ("title", "short_description")


translator.register(ProjectType, ProjectTypeTranslationOptions)
simple_history.register(ProjectType)


class ProjectTranslationOptions(TranslationOptions):
    fields = ("title", "short_description")


translator.register(Project, ProjectTranslationOptions)
simple_history.register(Project)
