from urllib.parse import parse_qs, urlencode

from django import template
from django.utils.html import format_html

register = template.Library()


class BuildQueryStringNode(template.Node):
    def __init__(self, sortfield):
        self.sortfield = sortfield
        super(BuildQueryStringNode, self).__init__()

    def render(self, context):
        qs = parse_qs(context['current_query'])
        if 'sort' in qs and self.sortfield in qs['sort']:
            if self.sortfield.startswith('-'):
                qs['sort'] = [self.sortfield[1:]]
            else:
                qs['sort'] = ['-' + self.sortfield]
        else:
            qs['sort'] = [self.sortfield]
        return urlencode(qs, True).replace('&', '&amp;')


@register.tag(name='buildsortqs')
def do_buildsortqs(parser, token):
    try:
        _, sortfield = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token)
    if not (sortfield[0] == sortfield[-1] and sortfield[0] in ('"', "'")):
        raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % token)
    return BuildQueryStringNode(sortfield[1:-1])


@register.simple_tag
def pkg_details_link(pkg, link_title=None, honor_flagged=False):
    if not pkg:
        return link_title or ''
    if link_title is None:
        link_title = pkg.pkgname
    link_content = link_title
    if honor_flagged and pkg.flag_date:
        link_content = '<span class="flagged">%s</span>' % link_title
    link = '<a href="%s" title="View package details for %s">%s</a>'
    return format_html(link % (pkg.get_absolute_url(), pkg.pkgname, link_content))


# vim: set ts=4 sw=4 et:
