import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse


class WheelInstallerNode:
    """
    A ComfyUI node that installs Python wheels from URLs.
    URLs are loaded from wheel_urls.txt in the node directory.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define the input types for the node.
        Returns a dictionary with required and optional inputs.
        """
        # Get the directory where this node file is located
        node_dir = Path(__file__).parent
        urls_file = node_dir / "wheel_urls.txt"

        # Load wheel URLs from the configuration file
        wheel_options = cls._load_wheel_urls(urls_file)

        return {
            "required": {
                "wheel_url": (wheel_options, {
                    "default": wheel_options[0] if wheel_options else ""
                }),
                "force_reinstall": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Yes",
                    "label_off": "No"
                }),
            },
        }

    @classmethod
    def _load_wheel_urls(cls, urls_file):
        """
        Load wheel URLs from the configuration file.

        Args:
            urls_file: Path to the wheel_urls.txt file

        Returns:
            List of wheel URLs (with filenames as display text)
        """
        urls = []

        if not urls_file.exists():
            print(f"Warning: {urls_file} not found. Creating default file.")
            urls_file.write_text(
                "# Add wheel URLs here, one per line\n"
                "# Lines starting with # are comments\n"
            )
            return ["No wheels configured"]

        try:
            with open(urls_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        urls.append(line)
        except Exception as e:
            print(f"Error reading {urls_file}: {e}")
            return [f"Error reading config: {e}"]

        if not urls:
            return ["No wheels configured"]

        return urls

    @classmethod
    def _extract_filename(cls, url):
        """
        Extract the filename from a URL.

        Args:
            url: The wheel URL

        Returns:
            The filename portion of the URL
        """
        parsed = urlparse(url)
        return Path(parsed.path).name or url

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("status_message", "success")
    FUNCTION = "install_wheel"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def install_wheel(self, wheel_url, force_reinstall=False):
        """
        Install a Python wheel from the specified URL.

        Args:
            wheel_url: URL to the wheel file
            force_reinstall: Whether to force reinstallation

        Returns:
            Tuple of (status_message, success)
        """
        # Check if this is an error/warning message
        if wheel_url.startswith("No wheels") or wheel_url.startswith("Error"):
            return (wheel_url, False)

        try:
            # Build the pip install command
            cmd = [sys.executable, "-m", "pip", "install"]

            if force_reinstall:
                cmd.append("--force-reinstall")

            cmd.append(wheel_url)

            # Execute the installation
            print(f"Installing wheel: {wheel_url}")
            print(f"Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            # Check the result
            if result.returncode == 0:
                filename = self._extract_filename(wheel_url)
                success_msg = f"Successfully installed: {filename}"
                print(success_msg)
                print(result.stdout)
                return (success_msg, True)
            else:
                error_msg = f"Failed to install wheel. Error: {result.stderr}"
                print(error_msg)
                return (error_msg, False)

        except subprocess.TimeoutExpired:
            error_msg = "Installation timed out (exceeded 5 minutes)"
            print(error_msg)
            return (error_msg, False)

        except Exception as e:
            error_msg = f"Error during installation: {str(e)}"
            print(error_msg)
            return (error_msg, False)


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "WheelInstaller": WheelInstallerNode
}

# Display name mappings for ComfyUI
NODE_DISPLAY_NAME_MAPPINGS = {
    "WheelInstaller": "Wheel Installer"
}
