from django.db import models


class SeedTracker(models.Model):
    '''
    Note: This model is a temporary solution intended to help prevent duplicate database seeding for `ad_group_stats`.
    This is necessary because entries in the `ad_group_stats` table do not have a unique identifier.

    Both `campaign` and `ad_group` tables have unique identifiers (`campaign_id` and `ad_group_id`, respectively).
    Error handling has therefore been implemented for the seeding process of both tables.
    '''

    name = models.CharField(max_length=255)
    seeded = models.BooleanField(default=True)
