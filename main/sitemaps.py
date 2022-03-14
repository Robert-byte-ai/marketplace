from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy

from .models import Ad


class AdSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Ad.objects.filter(is_archive=False)

    def location(self, obj):
        return reverse_lazy('ad', args=(obj.id,))
