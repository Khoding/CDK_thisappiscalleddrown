from django import template

from ..models import Inscription

register = template.Library()


@register.inclusion_tag("thisappiscalleddrown/entry_snippet.html")
def render_latest_blog_entries(
    num, summary_first=False, hide_readmore=False, hide_header=False, show_reason="", header_tag=""
):
    entries = Inscription.objects.all()
    return {
        "entries": entries,
        "summary_first": summary_first,
        "header_tag": header_tag,
        "show_reason": show_reason,
        "hide_header": hide_header,
        "hide_readmore": hide_readmore,
    }
