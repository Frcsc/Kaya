import logging
import os

import pandas as pd
from django.conf import settings
from django.db import transaction

from campaign.models import Campaign

logger = logging.getLogger(__name__)


FILE_PATH = os.path.join(settings.BASE_DIR, 'seeding', 'csv', 'campaign.csv')


class SeedCampaignTable:
    def load_campaign_table(self):

        try:
            df = pd.read_csv(FILE_PATH)
        except Exception as e:
            logger.error(f"Error reading CSV file: {e}")
            return False

        with transaction.atomic():
            for _, row in df.iterrows():
                try:
                    Campaign.objects.update_or_create(
                        campaign_id=row['campaign_id'],
                        defaults={
                            "campaign_name": row['campaign_name'],
                            "campaign_type": row['campaign_type'],
                        },
                    )
                except Exception as e:
                    logger.error(f"Error inserting row {row['campaign_id']}: {e}")
                    return False

        return True
