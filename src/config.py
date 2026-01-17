import os
from pathlib import Path

from dotenv import load_dotenv

# load environment variables from a .env file if it exists
load_dotenv()

my_username = os.getenv("MDWIKI_USERNAME", "")
mdwiki_pass = os.getenv("MDWIKI_PASSWORD", "")
MAIN_PATH = os.getenv("EDITORS_STATS_PATH", "")

main_dump_path = Path(MAIN_PATH) if MAIN_PATH else Path("/tmp") / "editors_stats_dump"

editors_dump_path = main_dump_path / "editors"
sites_path = main_dump_path / "sites"

main_dump_path.mkdir(exist_ok=True)
editors_dump_path.mkdir(exist_ok=True)
sites_path.mkdir(exist_ok=True)
