from urllib.parse import quote as urlquote
from urllib.parse import unquote, urlencode

from django import template
from django.conf import settings
from django.utils.html import format_html

from main.templatetags import pgp
from main.utils import gitlab_project_name_to_path

register = template.Library()


def link_encode(url, query):
    # massage the data into all utf-8 encoded strings first, so urlencode
    # doesn't barf at the data we pass it
    query = {k: str(v).encode('utf-8') for k, v in query.items()}
    data = urlencode(query)
    return "%s?%s" % (url, data)


@register.simple_tag
def details_link(pkg):
    link = '<a href="%s" title="View package details for %s">%s</a>'
    return format_html(link % (pkg.get_absolute_url(), pkg.pkgname, pkg.pkgname))


@register.simple_tag
def scm_link(package, operation: str):
    parts = (operation, package.pkgbase)
    linkbase = ("https://github.com/z3ntu/archhurd_packages/%s/master/%s")
    return linkbase % tuple(urlquote(part.encode('utf-8')) for part in parts)


@register.simple_tag
def bugs_list(package):
    url = "https://github.com/z3ntu/archhurd_packages/issues"
    data = {
        'q': 'is:issue is:open [%s]' % package.pkgname,
    }
    return link_encode(url, data)


@register.simple_tag
def bug_report(package):
    url = "https://github.com/z3ntu/archhurd_packages/issues/new"
    data = {
        'title': '[%s] PLEASE ENTER SUMMARY' % package.pkgname,
    }
    return link_encode(url, data)


@register.simple_tag
def wiki_link(package):
    url = "https://wiki.archlinux.org/title/Special:Search"
    data = {
        'search': package.pkgname,
    }
    return link_encode(url, data)


@register.simple_tag
def man_link(package):
    url = "https://man.archlinux.org/listing/{}"
    return url.format(package.pkgname)


@register.simple_tag
def sec_link(package):
    url = "https://security.archlinux.org/package/{}"
    return url.format(package.pkgname)


@register.simple_tag
def rebuilderd_diffoscope_link(rbstatus):
    url = "https://reproducible.archlinux.org/api/v0/builds/{}/diffoscope"
    return url.format(rbstatus.build_id)


@register.simple_tag
def rebuilderd_buildlog_link(rbstatus):
    url = "https://reproducible.archlinux.org/api/v0/builds/{}/log"
    return url.format(rbstatus.build_id)


@register.simple_tag
def pgp_key_link(key_id, link_text=None):
    return pgp.pgp_key_link(key_id, link_text)


@register.filter
def url_unquote(original_url):
    return unquote(original_url)

# vim: set ts=4 sw=4 et:
