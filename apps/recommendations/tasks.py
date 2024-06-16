from celery import shared_task
from celery.utils.log import get_task_logger

from apps.recommendations.helpers import update_restaurant_data_from_google_places

logger = get_task_logger(__name__)


@shared_task(max_retries=3)
def fetch_restaurant_data_from_google_places():
    """
    Celery task to fetch restaurant data from Google Places API.
    This will be used for recommendations.
    :return:
    """
    try:
        update_restaurant_data_from_google_places()
        return True
    except Exception as e:
        logger.error(f"Task failed: {e}")
        return False
