from django.contrib.syndication.views import Feed

from .models import Activity


class GroupActivityFeed(Feed):
    """
    Flux RSS des activités de groupe.
    """

    title = "Activités thisappiscalleddrown"
    link = ""
    description = "Vos activités thisappiscalleddrown"

    def items(self):
        """
        Objets
        """

        return Activity.objects.all()

    def item_title(self, item):
        """
        Titre de l'objet.
        """

        return item.name

    def item_description(self, item):
        """
        Description de l'objet
        """

        return item.description

    def item_link(self, item):
        """
        Lien vers l'ibjet
        """

        return item.get_absolute_url()

    def item_pubdate(self, item):
        """
        Date de publication.
        """

        return item.start_date

    def item_author_name(self, item):
        """
        Nom de l'auteur.
        """

        return item.creator
