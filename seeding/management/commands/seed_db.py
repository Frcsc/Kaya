import logging

from django.core.management.base import BaseCommand

from ad_group.mixins import SeedAdGroupTable
from ad_group_stats.mixins import SeedAdGroupStatTable
from campaign.mixins import SeedCampaignTable
from seeding.models import SeedTracker

logger = logging.getLogger(__name__)


class Command(BaseCommand, SeedCampaignTable, SeedAdGroupTable, SeedAdGroupStatTable):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        campaingn_seeding = self.load_campaign_table()

        if campaingn_seeding is False:
            self.stdout.write(self.style.ERROR("Error during campaign table seeding"))
            return
        self.stdout.write(self.style.SUCCESS("Campaign seeding is DONE"))

        ad_group_seeding = self.load_ad_group_table()

        if ad_group_seeding is False:
            self.stdout.write(self.style.ERROR("Error during Ad group table seeding"))
            return
        self.stdout.write(self.style.SUCCESS("Ad group seeding is DONE"))

        if SeedTracker.objects.filter(seeded=True).exists():

            self.stdout.write(
                self.style.WARNING(
                    "Seeding has already been performed for ad_group_stats"
                )
            )
            return

        ad_group_stats_seeding = self.load_ad_group_stats_table()

        if ad_group_stats_seeding is False:
            self.stdout.write(self.style.ERROR("Error during Ad group table seeding"))
            return

        SeedTracker.objects.create(name='seeded_once')

        self.stdout.write(self.style.SUCCESS("Ad group stats seeding is DONE"))

        self.stdout.write(self.style.SUCCESS("Seeding Complete"))
