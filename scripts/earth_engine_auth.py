import ee
from ee import ServiceAccountCredentials
import os
import logging

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def authenticate(
    service_account: str = 'test-service-account@ee-gabrieldiazireland.iam.gserviceaccount.com',
    key_path: str = '../scripts/earthengine-key.json',
    project_id: str = 'ee-gabrieldiazireland'
):
    """Authenticate Earth Engine using a service account."""
    try:
        logging.info(f"🔐 Using service account: {service_account}")
        if not os.path.exists(key_path):
            raise FileNotFoundError(f"❌ Key file not found at: {key_path}")

        logging.info(f"📂 Loading key from: {key_path}")
        credentials = ServiceAccountCredentials(service_account, key_path)

        logging.info("🌍 Initializing Earth Engine...")
        ee.Initialize(credentials, project=project_id)

        logging.info("✅ Earth Engine initialized successfully.")
    except Exception as e:
        logging.error(f"🚨 Initialization failed: {e}")
        raise

