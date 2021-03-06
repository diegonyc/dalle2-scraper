"""
Script to start the dalle2 generations extraction process.
"""

import os
import logging

from dotenv import load_dotenv
import requests

from extractor.algolia_storage import AlgoliaGenerationRepository
from extractor.subreddit_crawler import SubredditCrawler


# TODO: Refactor extract into run script with extract, load, and
# transform subscripts.
if __name__ == "__main__":
    load_dotenv()

    generation_repository = AlgoliaGenerationRepository(
        app_id=os.getenv("ALGOLIA_APP_ID"),
        api_key=os.getenv("ALGOLIA_API_KEY"),
        generation_index=os.getenv("ALGOLIA_STORAGE_INDEX"),
    )

    crawler_config = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "user_agent": os.getenv("CLIENT_USER_AGENT"),
        "reddit_username": os.getenv("REDDIT_USERNAME"),
        "reddit_password": os.getenv("REDDIT_PASSWORD"),
    }
    crawler = SubredditCrawler("dalle2", **crawler_config)

    openai_ids = crawler.crawl()

    OPEN_AI_BASE_URL = "https://labs.openai.com"
    OPEN_AI_TEMPLATE_URL = f"{OPEN_AI_BASE_URL}/api/labs/public/generations/generation-"
    openai_generation_urls = map(lambda i: f"{OPEN_AI_TEMPLATE_URL}{i}", openai_ids,)

    for generation_url in openai_generation_urls:
        print(f"Generation URL: {generation_url}")

        try:
            response = requests.get(generation_url)
            assert response.status_code == 200
            generation_info = response.json()

            generation_item = {
                "objectID": generation_info["id"],
                "image_path": generation_info["generation"]["image_path"],
                "generation_prompt": generation_info["prompt"]["prompt"]["caption"],
                "author_name": generation_info["user"]["name"],
                "thumbnail_path": generation_info["generation"]["image_path"],
            }
        except Exception as e:
            logging.warning(
                f"""
Could not store item (error and item debug information printed below):

Item information: {generation_info}

====

Error: {e}
                """
            )
            continue
        else:
            generation_repository.store_generation(generation_item)
