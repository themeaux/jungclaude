"""Quick Qdrant Cloud connectivity test.

Usage:
    python test_qdrant_connection.py

Set QDRANT_API_KEY below (or export it as an environment variable)
before running. The key is intentionally not committed.
"""

import os

from qdrant_client import QdrantClient

QDRANT_URL = "https://90713eca-db9b-4e77-bd43-f2f6dd39dab5.us-west-2-0.aws.cloud.qdrant.io:6333"


def main() -> None:
    api_key = os.getenv("QDRANT_API_KEY", "local install")
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=api_key,
    )
    print(qdrant_client.get_collections())


if __name__ == "__main__":
    main()
