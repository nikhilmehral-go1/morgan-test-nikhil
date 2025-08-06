import os
import httpx
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Helper function to get OAuth token ---
def _get_oauth_token() -> str:
    """
    Placeholder function to get an OAuth token.
    In a real application, this would involve a proper OAuth2 flow.
    For now, it reads a static token from environment variables.
    """
    token = os.getenv("GO1_API_TOKEN")
    if not token:
        logger.error("GO1_API_TOKEN environment variable not set.")
        raise ValueError("Go1 API token is not configured.")
    return token

# --- Your Tool Function ---
def get_learning_objects_tool(keyword: str = "") -> str:
    """Get learning objects from Go1 API with optional keyword search."""
    try:
        token = _get_oauth_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "api-version": "alpha"
        }
        params = {}
        if keyword:
            params["keyword"] = keyword
            logger.debug(f"Searching with keyword: {keyword}")

        response = httpx.get(
            "https://gateway.go1.com/learning-objects",
            headers=headers,
            params=params
        )
        
        logger.debug(f"API response status: {response.status_code}")
        response.raise_for_status()
        
        data = response.json()
        hits = data.get('hits', [])
        total = data.get('total', 0)
        logger.info(f"Successfully retrieved {len(hits)} learning objects out of {total} total")

        if len(hits) > 0:
            titles = [hit.get('title') or hit.get('name') for hit in hits[:5]]
            search_info = f" for keyword '{keyword}'" if keyword else ""
            return f"Found {len(hits)} learning objects{search_info}. Titles: {' | '.join(titles)}"
        else:
            search_info = f" for keyword '{keyword}'" if keyword else ""
            return f"No learning objects found{search_info}."
            
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP {e.response.status_code} error: {e.response.text}")
        return f"An error occurred while fetching data from the Go1 API."
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"
