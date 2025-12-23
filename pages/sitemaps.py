from django.contrib.sitemaps import Sitemap
from pages import models
class FoodSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    def items(self):
        return models.Food.objects.all()