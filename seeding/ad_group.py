import logging
import os

import pandas as pd
from django.conf import settings
from django.db import transaction

from ad_group.models import AdGroup
from campaign.models import Campaign

logger = logging.getLogger(__name__)

FILE_PATH = os.path.join(settings.BASE_DIR, 'seeding', 'csv', 'ad_group.csv')


class SeedAdGroupTable:
    def load_ad_group_table(self):
        try:
            df = pd.read_csv(FILE_PATH)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return False

        campaigns = {
            campaign.campaign_id: campaign for campaign in Campaign.objects.all()
        }

        with transaction.atomic():
            for _, row in df.iterrows():
                campaign_instance = campaigns.get(f"{row['campaign_id']}")

                if not campaign_instance:
                    logger.error(
                        f"Campaign_id {row['campaign_id']} does not exist in the database"
                    )
                    return False

                try:
                    AdGroup.objects.update_or_create(
                        ad_group_id=row['ad_group_id'],
                        defaults={
                            "ad_group_name": row["ad_group_name"],
                            "campaign": campaign_instance,
                        },
                    )
                except Exception as e:
                    logger.error(f"Error inserting row {row['ad_group_id']}: {e}")
                    return False
        return True
