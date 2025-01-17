import requests
import platform
import zipfile
import os
import stat
from io import BytesIO
from urllib.parse import urljoin
from dotenv import set_key
from pathlib import Path

def setup_chromium(base_url: str = "https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.83/"):
    """
    Downloads the latest chromedriver binary and registers its path in the .env file. If .env does not exists, then creates one.
    """
    
    if not base_url.endswith("/"):
        base_url += "/"

    drivers_path = Path("drivers")
    n_bits = platform.architecture()[0].replace('bit', '')
    current_system = platform.system()
    systems = {
        "Linux":"linux64/chromedriver-linux64.zip",
        "Windows":f"win{n_bits}/chromedriver-win{n_bits}.zip"
    }

    url = urljoin(base_url, systems[current_system])
    response = requests.get(url)
    if response.status_code == 200:
        zipfiles = zipfile.ZipFile(BytesIO(response.content))
        driver_path = [f for f in zipfiles.namelist() if "/chromedriver" in f][0]
        driver_path = drivers_path.joinpath(driver_path)

        if not driver_path.exists():
            zipfiles.extractall(drivers_path)
        
        new_driver_path = driver_path.with_suffix(".exe")
        os.rename(driver_path, new_driver_path)
        os.chmod(new_driver_path, 0o755)

    else:
        raise ConnectionError(f"Tried a GET request at {url} but failed with code {response.status_code}")
    
    env_file_path = Path(".env")
    if not env_file_path.exists():
        env_file_path.touch(mode=0o600, exist_ok=False)
    set_key(dotenv_path=env_file_path, key_to_set="CHROME_EXECUTABLE", value_to_set=new_driver_path.as_posix())
