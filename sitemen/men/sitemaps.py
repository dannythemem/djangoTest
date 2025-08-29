from django.contrib.sitemaps import Sitemap#

from men.models import Men


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Men.published.all()

    def lastmod(self, obj):
        return obj.time_updated
