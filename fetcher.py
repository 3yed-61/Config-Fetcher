import requests
from urllib.parse import urlparse
import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

HEADERS = """//profile-title: base64:4pmo77iPM867zp7EkChPdXRsaW5lKQ==
//profile-update-interval: 24
//subscription-userinfo: upload=5368709120; download=445097156608; total=955630223360; expire=1762677732
//support-url: https://t.me/talk_to_3yed_bot
//profile-web-page-url: https://github.com/3yed-61"""

def fetch_config(url):
    https_url = url.replace('ssconf://', 'https://')
    logger.info(f"Fetching config from: {https_url}")
    
    try:
        response = requests.get(https_url, timeout=10)
        response.raise_for_status()
        content = response.text.strip()
        if content.startswith('ss://'):
            logger.info(f"Successfully fetched config from {https_url}")
            return content
        else:
            logger.error(f"Invalid config format from {https_url}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching {https_url}: {str(e)}")
        return None

def main():
    logger.info("Starting config fetch process")

    urls = [
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-1.csv",
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-2.csv",
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-3.csv",
        "ssconf://ainita.s3.eu-north-1.amazonaws.com/AinitaServer-4.csv"
    ]

    configs = []
    for url in urls:
        logger.info(f"Processing URL: {url}")
        config = fetch_config(url)
        if config:
            configs.append(config)
    
    if not configs:
        logger.error("No configs were successfully fetched!")
        sys.exit(1)

    try:
        with open('configs.txt', 'w', encoding='utf-8') as f:
            f.write(HEADERS)
            f.write('\n\n')
            f.write('\n'.join(configs))
        logger.info(f"Successfully wrote {len(configs)} configs to configs.txt with headers")
    except Exception as e:
        logger.error(f"Error writing to file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
