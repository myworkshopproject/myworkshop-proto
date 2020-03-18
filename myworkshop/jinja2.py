from babel import dates, numbers
from datetime import datetime, timezone
from django.conf import settings
from django.contrib.messages import get_messages
from django.templatetags.static import static
from django.urls import reverse
from django.utils import translation
from jinja2 import Environment
from markdown import markdown
from mimetypes import guess_type
from core.models import Image, ProjectType, Publication, PublicationType
from flatpages.models import FlatPage


def to_markdown(value):
    return markdown(value)


def get_image(id):
    try:
        image = Image.objects.get(pk=id)
        return image
    except:
        return None


def get_publication(slug):
    try:
        publication = Publication.objects.get(slug=slug)
        return publication
    except:
        return None


# babel : http://babel.pocoo.org/en/latest/
def format_date(value, format="medium", locale=settings.LANGUAGE_CODE):
    # format : one of : short, medium (the default), long and full
    return dates.format_date(value, format=format, locale=locale)


def format_datetime(value, format="medium", locale=settings.LANGUAGE_CODE):
    # format : one of : short, medium (the default), long and full
    return dates.format_datetime(value, format=format, locale=locale)


def format_time(value, format="medium", locale=settings.LANGUAGE_CODE):
    # format : one of : short, medium (the default), long and full
    return dates.format_time(value, format=format, locale=locale)


def format_timedelta(
    value, format="long", locale=settings.LANGUAGE_CODE, to=datetime.now(timezone.utc)
):
    # format : one of : narrow, long (the default) and short
    return dates.format_timedelta(to - value, format=format, locale=locale)


def format_number(number, locale=settings.LANGUAGE_CODE):
    return numbers.format_number(number, locale=locale)


def format_decimal(number, locale=settings.LANGUAGE_CODE, decimal_quantization=False):
    return numbers.format_decimal(
        number, locale=locale, decimal_quantization=decimal_quantization
    )


def format_currency(
    number,
    currency="EUR",
    format=None,
    locale=settings.LANGUAGE_CODE,
    currency_digits=True,
    format_type="standard",  # one of : standard (the default) and name
    decimal_quantization=True,
):
    return numbers.format_currency(
        number,
        currency=currency,
        format=format,
        locale=locale,
        currency_digits=currency_digits,
        format_type=format_type,
        decimal_quantization=decimal_quantization,
    )


def format_percent(
    number, format=None, locale=settings.LANGUAGE_CODE, decimal_quantization=False
):
    return numbers.format_percent(
        number, format=format, locale=locale, decimal_quantization=decimal_quantization
    )


def format_scientific(
    number, format=None, locale=settings.LANGUAGE_CODE, decimal_quantization=False
):
    return numbers.format_scientific(
        number, format=format, locale=locale, decimal_quantization=decimal_quantization
    )


def environment(**options):
    env = Environment(
        extensions=["jinja2.ext.i18n", "jinja2.ext.with_"],
        trim_blocks=True,
        lstrip_blocks=True,
        **options
    )
    languages = []
    for language in settings.LANGUAGES:
        languages.append(translation.get_language_info(language[0]))

    env.globals.update(
        {
            "get_messages": get_messages,
            "guess_type": guess_type,
            "languages": languages,
            "pages": FlatPage.objects.filter(level=0),
            "project_types": ProjectType.objects.all(),
            "publication_types": PublicationType.objects.all(),
            "settings": settings,
            "static": static,
            "translation": translation,
            "url": reverse,
            "get_image": get_image,
            "get_publication": get_publication,
        }
    )
    env.install_gettext_translations(translation)
    env.filters["format_date"] = format_date
    env.filters["format_datetime"] = format_datetime
    env.filters["format_time"] = format_time
    env.filters["format_timedelta"] = format_timedelta
    env.filters["format_number"] = format_number
    env.filters["format_decimal"] = format_decimal
    env.filters["format_currency"] = format_currency
    env.filters["format_percent"] = format_percent
    env.filters["format_scientific"] = format_scientific
    env.filters["to_markdown"] = to_markdown
    return env
