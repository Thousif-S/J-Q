from django.conf import settings
from django.db import models

# Create your models here.


class BaseWork(models.Model):

    DESIGNING_CATEGORY = 'ds'
    WEB_DEVELOPMENT_CATEGORY = 'wb'
    MEDICAL_CATEGORY = 'md'
    AGRICULTURAL_CATEGORY = 'ag'
    SYSTEM_ADMINISTRATION_CATEGORY = 'sa'

    WORK_CATEGORY = (
        (DESIGNING_CATEGORY, 'Designing'),
        (WEB_DEVELOPMENT_CATEGORY, 'Web Development'),
        (MEDICAL_CATEGORY, 'Medics'),
        (AGRICULTURAL_CATEGORY, 'Agricultural'),
        (SYSTEM_ADMINISTRATION_CATEGORY, 'Sys Admin')
    )

    title = models.CharField(max_length=150, verbose_name='Title')
    description = models.TextField(
        blank=True, null=True, verbose_name='Work Description')
    category = models.CharField(
        max_length=2, choices=WORK_CATEGORY, blank=True, null=True)
    posted_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Posted on')
    updated_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Updated on')
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)
    
    # status = models


class Quest(BaseWork):
    expiring_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title


class Job(BaseWork):
    about_us = models.TextField(verbose_name='About Us', blank=True, null=True)

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # job = models.ForeignKey('works.Job', related_name='votes',
    #                         on_delete=models.CASCADE, blank=True, null=True)
    quest = models.ForeignKey(
        'works.Quest', related_name='votes', on_delete=models.CASCADE, blank=True, null=True)
