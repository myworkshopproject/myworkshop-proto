# Technical details

> :warning: **attention** : ce document est en cours de rédaction.

## Idée principale
L'idée principale de cet outil repose sur deux types d'objets : les __publications__ et les __projets__.

Une __publication__ peut être un article de blog, un tutoriel, ou toute autre forme de document court détaillant un sujet simple.

Un __projet__ est un espace de collaboration permettant à ses contributeurs de collecter, de créer ou d'organiser des publications afin d'obtenir une documentation claire et organisée du projet.

Cette structure modulaire permet de lier à plusieurs projets une même publication afin de mutualiser la rédaction de documentation de projets.

Par exemple, un tutoriel détaillant l'utilisation d'une machine à découpe laser pourra apparaître sur la documentation d'un projet de robot ou sur la documentation d'un projet de fabrication de décorations de Noël.

### Publication
Lorsqu'un utilisateur crée un nouvel object `Publication`, il en devient automatiquement l'auteur (champ `Publication.owner` de type _ForeignKey_ vers un objet `CustomUser`).

Ce dernier doit être le seul à avoir des droits d'édition sur sa publication, à l'exception de l'attribut `Publication.visibility` que peut éditer un modérateur pour rendre publique ou non la publication après relecture.

Le champ `Publication.type` (de type _ForeignKey_ vers un objet `PublicationType`) permet d'attribuer à une nouvelle publication l'un des types prédéfinis sur le site (par exemple un article de blog, un tutoriel de fabrication, une fiche pédagogique, etc.).
Ce champ, défini à la création de l'objet, ne doit pas pouvoir être changé par la suite.

L'objet `Publication` comporte, entres autres, le champ `Publication.body` (de type _JSONField_) qui permet de structurer le contenu de la publication au format _JSON_ afin d'apporter une certaine souplesse en terme de présentation. Ainsi, un tutoriel sera en général constitué d'une série d'étapes numérotées constituées chacune d'une ou plusieurs images et d'un paragraphe de texte rédigé en language _markdown_. Quant à un article de blog, son contenu sera plutôt constitué d'une succession linéaire de paragraphes, d'images ou de liens.

### Project
Un projet est un espace permettant la collaboration de plusieurs utilisateurs autour d'un même sujet.

Plusieurs collaborateurs (champ `Project.contributors` de type _ManyToManyField_ vers des objets `CustomUser`, via la classe `ProjectContributor`) peuvent participer à un projet.
Un contributeur possède l'un des rôles suivants (via l'attribut `ProjectContributor.role`) :
* `OWNER` : a tous les droits sur le projet, notamment sur la gestions des contributeurs ;
* `EDITOR` : possède quelques droits d'édition (ajouter de nouvelles publications, des entrées de la forge, etc.).
* `CONTRIBUTOR` : une simple mention dans la liste des contributeurs, sans droit particulier.

Le créateur d'un projet se voit attribuer automatiquement le rôle `OWNER`.

Un projet dispose d'une _forge_ dans laquelle les contributeurs peuvent poster des images, du textes, des liens, etc. en prévision de la rédaction des publications.

Un projet dispose d'un espace _issues_ permettant aux contributeurs de remonter les problèmes rencontrés lors de la réalisation du projet. Ces problèmes pourront être, si besoin, affichés sur la page d’accueil du site pour faire appel à de nouveaux contributeurs.

Un projet dispose d'un espace de discussion public, le _forum_, pour faciliter les échanges entres les contributeurs d'un projet et le reste du monde !

## Fonctionnalités secondaires

### Le cahier de laboratoire
Le cahier de laboratoire, ou _labbook_ est un espace personnel, non public, permettant de prendre des notes au fil de l'eau (fonctions équivalentes à la _forge_ d'un projet). Il peut s'agir de photos, liens, notes, etc.

Ces notes pourront ensuite être réutilisées lors de la rédaction de publications.

### Le trombinoscope
Chaque utilisateur a la possibilité de rendre public tout ou partie de son profil comme la liste des projets auxquels il participe, ses publications, ses contributions, etc.
Son profil sera alors visible dans le trombinoscope du site.

## Internationalization
Une instance de _myworkshop_ peut être internationalisée, à la fois pour le contenu statique et pour le contenu dynamique. La liste des langues disponibles est définie dans `settings`.

Certains champs des publications et projets peuvent alors être traduit. À défaut de traduction disponible dans une langue spécifique, le contenu est affiché dans la langue principale du site.

_myworkshop_ utilise le paquet `django-modeltranslation` pour fournir des champs multilingues aux modèles.

## Versioning
Le paquet _django-simple-history_ est utilisé dès le départ. Même si l'implémentation est développée plus tard, l'historique aura été sauvegardé.

## API web
Il est prévu de développer une _API web RESt_ à l'aide du paquet `django-rest-framework` afin de mettre en place un réseau _peer to peer_ de partage de publications entres plusieurs instances de _myworkshop_.

## Accessibilité
Une attention particulière est portée à l'accessibilité du site web afin de permettre aux utilisateurs malvoyant d'utiliser leurs outils d'accessibilité ou aux utilisateurs de mobile d'avoir un accès facile à l'ensemble des fonctions du site.

## Authentification et permissions
L'authentification des utilisateurs repose principalement sur le paquet `django-allauth`, dont les templates sont surchargées dans l'application `apps/accounts`.
