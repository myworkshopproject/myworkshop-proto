import re
import requests
from bs4 import BeautifulSoup, SoupStrainer
from bs4.dammit import EncodingDetector
from urllib.parse import urlparse
from django.core.validators import RegexValidator
from django.utils.translation import gettext, gettext_lazy as _


class UsernameValidator(RegexValidator):
    regex = r"^[\w]+\Z"
    message = _(
        "Enter a valid username. This value may contain only letters, numbers, and _ character."
    )
    flags = 0


class TwitterUsernameValidator(RegexValidator):
    regex = r"^@[\w]+\Z"
    message = _(
        "Enter a valid Twitter username. This value may start with @ and contain only letters, numbers, and _ character."
    )
    flags = 0


# notes:
# * doit-on se limiter à certains domaines d'url ?
# * doit-on récupérer « favicon » ?


def custom_url_parse(url):

    data = {
        "title": "unknown",
        "type": "website",
        "description": "",
        "tags": "",
        "url": url,
        "site_name": urlparse(url).netloc,
    }
    # https://stackoverflow.com/questions/9626535/get-protocol-host-name-from-url

    try:
        # note: on n'utilise pas le header « user_agent »
        headers = {"Accept-Language": "fr, en;q=0.9, de;q=0.9, *;q=0.5"}
        response = requests.get(url, headers=headers)
    except:
        data["error"] = str(response.status_code)
        return data

    if response.status_code != requests.codes.ok:
        data["error"] = str(response.status_code)
        return data

    # note: on essaye de deviner au mieux l'encodage de la page
    # https://stackoverflow.com/questions/7219361/python-and-beautifulsoup-encoding-issues
    http_encoding = (
        response.encoding
        if "charset" in response.headers.get("content-type", "").lower()
        else None
    )
    html_encoding = EncodingDetector.find_declared_encoding(
        response.content, is_html=True
    )
    encoding = html_encoding or http_encoding

    # on ne parse que les balise « meta » et la balise « title » pour limiter les besoins en mémoire
    only_meta_and_title_tags = SoupStrainer(["meta", "title"])

    doc = BeautifulSoup(
        response.content,
        "lxml",
        from_encoding=encoding,
        parse_only=only_meta_and_title_tags,
    )

    # « title »
    # on cherche dans l'ordre :
    #   <meta content="..." property="og:title"/>
    #   <meta content="..." name="twitter:title"/>
    #   <meta content="..." property="twitter:title"/>
    #   <meta content="..." name="title"/>
    #   <title>...</title>
    # default : "unknown"
    og_tag = doc.find("meta", property="og:title")
    if og_tag and og_tag["content"]:
        data["title"] = og_tag["content"]
    else:
        og_tag = doc.find("meta", attrs={"name": "twitter:title"})
        if og_tag and og_tag["content"]:
            data["title"] = og_tag["content"]
        else:
            og_tag = doc.find("meta", property="twitter:title")
            if og_tag and og_tag["content"]:
                data["title"] = og_tag["content"]
            else:
                og_tag = doc.find("meta", attrs={"name": "title"})
                if og_tag and og_tag["content"]:
                    data["title"] = og_tag["content"]
                else:
                    if doc.title:
                        data["title"] = doc.title.string

    # « type »
    # on cherche la balise opengraph :
    #    <meta content="..." property="og:type"/>
    # default : "website"
    og_tag = doc.find("meta", property="og:type")
    if og_tag and og_tag["content"]:
        data["type"] = og_tag["content"]

    data["root_type"] = data["type"].split(".")[0]

    # « description »
    # on cherche dans l'ordre :
    #   <meta content="" property="og:description"/>
    #   <meta content="..." name="twitter:description"/>
    #   <meta content="..." property="twitter:description"/>
    #   <meta content="..." name="description"/>
    # default : ""
    og_tag = doc.find("meta", property="og:description")
    if og_tag and og_tag["content"]:
        data["description"] = og_tag["content"]
    else:
        og_tag = doc.find("meta", attrs={"name": "twitter:description"})
        if og_tag and og_tag["content"]:
            data["description"] = og_tag["content"]
        else:
            og_tag = doc.find("meta", property="twitter:description")
            if og_tag and og_tag["content"]:
                data["description"] = og_tag["content"]
            else:
                og_tag = doc.find("meta", attrs={"name": "description"})
                if og_tag and og_tag["content"]:
                    data["description"] = og_tag["content"]

    # « tags »
    # on cherche dans l'ordre :
    #   <meta content="..." property="*:tag"/>
    #   <meta content="..." name="keywords"/>
    # default : ""
    og_tags = doc.find_all("meta", property=re.compile(r"^[a-z,:]+:tag$"))
    tag_list = []
    if og_tags:
        for og_tag in og_tags:
            if og_tag and og_tag["content"]:
                tag_list.append(og_tag["content"])
    if tag_list:
        data["tags"] = tag_list
    else:
        keywords_meta_tag = doc.find("meta", attrs={"name": "keywords"})
        if keywords_meta_tag and keywords_meta_tag["content"]:
            data["tags"] = keywords_meta_tag["content"].split(",")

    # « url »
    # on cherche :
    #   <meta content="..." property="og:url"/>
    # default : url
    og_tag = doc.find("meta", property="og:url")
    if og_tag and og_tag["content"]:
        data["url"] = og_tag["content"]

    # « image »
    # on cherche :
    #    <meta content="..." property="og:image"/>
    #       puis on cherche :
    #           <meta content="..." property="og:image:width"/>
    #           <meta content="..." property="og:image:height"/>
    #           <meta content="..." property="og:image:alt"/>
    #    <meta content="..." title="twitter:image"/>
    #       puis on cherche :
    #           <meta content="..." title="twitter:image:width"/>
    #           <meta content="..." title="twitter:image:height"/>
    #           <meta content="..." title="twitter:image:alt"/>
    #    <meta content="..." property="twitter:image"/>
    #       puis on cherche :
    #           <meta content="..." property="twitter:image:width"/>
    #           <meta content="..." property="twitter:image:height"/>
    #           <meta content="..." property="twitter:image:alt"/>
    # default : None
    image = {}
    og_tag = doc.find("meta", property="og:image")
    if og_tag and og_tag["content"]:
        # url
        image["url"] = og_tag["content"]
        # width
        og_tag = doc.find("meta", property="og:image:width")
        if og_tag and og_tag["content"]:
            try:
                image["width"] = int(og_tag["content"])
            except:
                pass
        # height
        og_tag = doc.find("meta", property="og:image:height")
        if og_tag and og_tag["content"]:
            try:
                image["height"] = int(og_tag["content"])
            except:
                pass
        # alt
        og_tag = doc.find("meta", property="og:image:alt")
        if og_tag and og_tag["content"]:
            image["alt"] = og_tag["content"]
    else:
        og_tag = doc.find("meta", attrs={"name": "twitter:image"})
        if og_tag and og_tag["content"]:
            # url
            image["url"] = og_tag["content"]
            # width
            og_tag = doc.find("meta", attrs={"name": "twitter:image:width"})
            if og_tag and og_tag["content"]:
                try:
                    image["width"] = int(og_tag["content"])
                except:
                    pass
            # height
            og_tag = doc.find("meta", attrs={"name": "twitter:image:height"})
            if og_tag and og_tag["content"]:
                try:
                    image["height"] = int(og_tag["content"])
                except:
                    pass
            # alt
            og_tag = doc.find("meta", attrs={"name": "twitter:image:alt"})
            if og_tag and og_tag["content"]:
                image["alt"] = og_tag["content"]
        else:
            og_tag = doc.find("meta", property="twitter:image")
            if og_tag and og_tag["content"]:
                # url
                image["url"] = og_tag["content"]
                # width
                og_tag = doc.find("meta", property="twitter:image:width")
                if og_tag and og_tag["content"]:
                    try:
                        image["width"] = int(og_tag["content"])
                    except:
                        pass
                # height
                og_tag = doc.find("meta", property="twitter:image:height")
                if og_tag and og_tag["content"]:
                    try:
                        image["height"] = int(og_tag["content"])
                    except:
                        pass
                # alt
                og_tag = doc.find("meta", property="twitter:image:alt")
                if og_tag and og_tag["content"]:
                    image["alt"] = og_tag["content"]

    if image:
        data["image"] = image

    # « site_name »
    # on cherche dans l'ordre :
    #   <meta content="..." property="og:site_name"/>
    # default : netloc
    og_tag = doc.find("meta", property="og:site_name")
    if og_tag and og_tag["content"]:
        data["site_name"] = og_tag["content"]

    # on recherche les balise opengraph supplémentaires
    # « locale »
    # default : None
    og_tag = doc.find("meta", property="og:locale")
    if og_tag and og_tag["content"]:
        data["locale"] = og_tag["content"]

    # « locale_alternates »
    og_tags = doc.find_all("meta", property="og:locale:alternate")
    if og_tags:
        locale_alternates = []
        for og_tag in og_tags:
            if og_tag["content"]:
                locale_alternates.append(og_tag["content"])
        if locale_alternates:
            data["locale_alternates"] = locale_alternates

    # « video »
    # si le type est « video* », alors on recherche :
    #   <meta content="" property="og:video:secure_url"/>
    #   <meta content="" property="og:video:url"/>
    #   alors on recherche :
    #      <meta content="..." property="og:video:type"/>
    #      <meta content="..." property="og:video:width"/>
    #      <meta content="..." property="og:video:height"/>
    # default : None
    if data["root_type"] == "video":
        video = {}
        og_tag = doc.find("meta", property="og:video:secure_url")
        if og_tag and og_tag["content"]:
            video["url"] = og_tag["content"]
        else:
            og_tag = doc.find("meta", property="og:video:url")
            if og_tag and og_tag["content"]:
                video["url"] = og_tag["content"]

        if video:
            og_tag = doc.find("meta", property="og:video:type")
            if og_tag and og_tag["content"]:
                video["type"] = og_tag["content"]

            og_tag = doc.find("meta", property="og:video:width")
            if og_tag and og_tag["content"]:
                try:
                    video["width"] = int(og_tag["content"])
                except:
                    pass

            og_tag = doc.find("meta", property="og:video:height")
            if og_tag and og_tag["content"]:
                try:
                    video["height"] = int(og_tag["content"])
                except:
                    pass

            data["video"] = video

    # « audio »
    # si le type est « music* », alors on recherche :
    #   <meta content="" property="og:audio:secure_url"/>
    #   <meta content="" property="og:audio:url"/>
    #   alors on recherche :
    #      <meta content="..." property="og:audio:type"/>
    # default : None
    if data["root_type"] == "music":
        audio = {}
        og_tag = doc.find("meta", property="og:audio:secure_url")
        if og_tag and og_tag["content"]:
            audio["url"] = og_tag["content"]
        else:
            og_tag = doc.find("meta", property="og:audio:url")
            if og_tag and og_tag["content"]:
                audio["url"] = og_tag["content"]

        if audio:
            og_tag = doc.find("meta", property="og:audio:type")
            if og_tag and og_tag["content"]:
                audio["type"] = og_tag["content"]

            data["audio"] = audio

    # « embed »
    # si « type » est « video* » ou « music* », on recherche dans l'ordre
    #    <meta content="player" name="twitter:card"/>
    #    ou
    #    <meta content="audio" name="twitter:card"/>
    #    alors, on recherche :
    #       <meta content="..." name="twitter:player"/>
    #          alors, on recherche :
    #             <meta content="..." name="twitter:player:width"/>
    #             <meta content="..." name="twitter:player:height"/>
    #    <meta content="player" property="twitter:card"/>
    #    ou
    #    <meta content="audio" property="twitter:card"/>
    #    alors, on recherche :
    #       <meta content="..." property="twitter:player"/>
    #          alors, on recherche :
    #             <meta content="..." property="twitter:player:width"/>
    #             <meta content="..." property="twitter:player:height"/>
    # default : None
    if data["root_type"] in ["video", "music"]:
        # y-a-t-il du contenu « twitter player » ?
        twitter_card_player_tag = doc.find(
            "meta", attrs={"name": "twitter:card", "content": "player"}
        )
        twitter_card_audio_tag = doc.find(
            "meta", attrs={"name": "twitter:card", "content": "audio"}
        )
        if twitter_card_player_tag or twitter_card_audio_tag:
            twitter_player_tag = doc.find("meta", attrs={"name": "twitter:player"})
            if twitter_player_tag and twitter_player_tag["content"]:
                data["player"] = twitter_player_tag["content"]

        else:
            # certain sites utilisent la clé « property » au lieu de « name »
            twitter_card_player_tag = doc.find(
                "meta", attrs={"property": "twitter:card", "content": "player"}
            )
            twitter_card_audio_tag = doc.find(
                "meta", attrs={"property": "twitter:card", "content": "audio"}
            )
            if twitter_card_player_tag or twitter_card_audio_tag:
                twitter_player_tag = doc.find(
                    "meta", attrs={"property": "twitter:player"}
                )
                if twitter_player_tag and twitter_player_tag["content"]:
                    data["player"] = twitter_player_tag["content"]

    return data
