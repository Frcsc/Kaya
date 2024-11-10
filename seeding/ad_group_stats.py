import logging
import os

import pandas as pd
from django.conf import settings
from django.db import transaction

from ad_group.models import AdGroup
from ad_group_stats.models import AdGroupStat

logger = logging.getLogger(__name__)


FILE_PATH = os.path.join(settings.BASE_DIR, 'seeding', 'csv', 'ad_group_stats.csv')


class SeedAdGroupStatTable:
    def load_ad_group_stats_table(self):
        try:
            df = pd.read_csv(FILE_PATH)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return False

        ad_groups = {
            ad_group.ad_group_id: ad_group for ad_group in AdGroup.objects.all()
        }

        with transaction.atomic():
            for _, row in df.iterrows():
                ad_group_instance = ad_groups.get(f"{row['ad_group_id']}")

                if not ad_group_instance:
                    logger.error(
                        f"Ad_group_id: {row['ad_group_id']} does not exist in the database"
                    )
                    return False

                try:
                    AdGroupStat.objects.create(
                        date=row['date'],
                        ad_group=ad_group_instance,
                        device=row['device'],
                        impressions=row['impressions'],
                        clicks=row['clicks'],
                        conversions=row['conversions'],
                        cost=row['cost'],
                    )
                except Exception as e:
                    logger.error(
                        f"Error occured during Ad group stats creation due to this: {e}"
                    )
                    return False
        return True
