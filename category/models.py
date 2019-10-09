from django.db import models


''' ICL CONTACT CATEGORY '''

class ICL_ContactCategoryModel(models.Model):
    name = models.CharField(max_length=255)
    
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'ICL Contact Category'
        verbose_name_plural = 'ICL Contact Categories'

    def __str__(self):
        return self.name

''' SHS CONTACT CATEGORY '''


class SHS_ContactCategoryModel(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'SHS Contact Category'
        verbose_name_plural = 'SHS Contact Categories'

    def __str__(self):
        return self.name


''' IHE CONTACT CATEGORY '''


class IHE_ContactCategoryModel(models.Model):

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'IHE Contact Category'
        verbose_name_plural = 'IHE Contact Categories'

    def __str__(self):
        return self.name




