from django.contrib import sitemaps
from django.urls import reverse


class MainSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'monthly'
    protocol = 'https'

    def items(self):
        return ['home', 'joining', 'typical_day', 'what_is_gliding', 'faq', 'about', 'photologue:pl-gallery-archive', ]

    def location(self, obj):
        return reverse(obj)


# TODO: Generate blog sitemaps properly
class BlogSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['']

    def location(self, obj):
        return '/blog/'
