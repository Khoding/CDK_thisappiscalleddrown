from django.contrib.syndication.views import Feed
from django.utils import timezone

from .models import Activity, Group


class GroupActivitiesFeed(Feed):
    title = 'Activités Koolapic'
    link = ''
    description = 'Vos activités Koolapic'

    def items(self):
        return Activity.objects.all()

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.start_date

    def item_author_name(self, item):
        return item.creator
