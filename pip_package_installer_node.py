import os
import subprocess
import sys
from pathlib import Path


class PipPackageInstallerNode:
    """
    A ComfyUI node that installs pip packages by name.
    Package names are loaded from package_names.txt in the node directory.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define the input types for the node.
        Returns a dictionary with required and optional inputs.
        """
        # Get the directory where this node file is located
        node_dir = Path(__file__).parent
        packages_file = node_dir / "package_names.txt"

        # Load package names from the configuration file
        package_options = cls._load_package_names(packages_file)

        return {
            "required": {
                "package_name": (package_options, {
                    "default": package_options[0] if package_options else ""
                }),
                "force_reinstall": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Yes",
                    "label_off": "No"
                }),
                "upgrade": ("BOOLEAN", {
                    "default": False,
                    "label_on": "Yes",
                    "label_off": "No"
                }),
            },
        }

    @classmethod
    def _load_package_names(cls, packages_file):
        """
        Load package names from the configuration file.

        Args:
            packages_file: Path to the package_names.txt file

        Returns:
            List of package names
        """
        packages = []

        if not packages_file.exists():
            print(f"Warning: {packages_file} not found. Creating default file.")
            packages_file.write_text(
                "# Add package names here, one per line\n"
                "# Lines starting with # are comments\n"
                "# You can specify versions: numpy==1.24.0\n"
            )
            return ["No packages configured"]

        try:
            with open(packages_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if line and not line.startswith('#'):
                        packages.append(line)
        except Exception as e:
            print(f"Error reading {packages_file}: {e}")
            return [f"Error reading config: {e}"]

        if not packages:
            return ["No packages configured"]

        return packages

    RETURN_TYPES = ("STRING", "BOOLEAN")
    RETURN_NAMES = ("status_message", "success")
    FUNCTION = "install_package"
    CATEGORY = "utils"
    OUTPUT_NODE = True

    def install_package(self, package_name, force_reinstall=False, upgrade=False):
        """
        Install a pip package by name.

        Args:
            package_name: Name of the package to install
            force_reinstall: Whether to force reinstallation
            upgrade: Whether to upgrade the package if already installed

        Returns:
            Tuple of (status_message, success)
        """
        # Check if this is an error/warning message
        if package_name.startswith("No packages") or package_name.startswith("Error"):
            return (package_name, False)

        try:
            # Build the pip install command
            cmd = [sys.executable, "-m", "pip", "install"]

            if force_reinstall:
                cmd.append("--force-reinstall")

            if upgrade:
                cmd.append("--upgrade")

            cmd.append(package_name)

            # Execute the installation
            print(f"Installing package: {package_name}")
            print(f"Command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout (some packages are large)
            )

            # Check the result
            if result.returncode == 0:
                success_msg = f"Successfully installed: {package_name}"
                print(success_msg)
                if result.stdout:
                    print(result.stdout)
                return (success_msg, True)
            else:
                error_msg = f"Failed to install package. Error: {result.stderr}"
                print(error_msg)
                return (error_msg, False)

        except subprocess.TimeoutExpired:
            error_msg = "Installation timed out (exceeded 10 minutes)"
            print(error_msg)
            return (error_msg, False)

        except Exception as e:
            error_msg = f"Error during installation: {str(e)}"
            print(error_msg)
            return (error_msg, False)


# Node class mappings for ComfyUI
NODE_CLASS_MAPPINGS = {
    "PipPackageInstaller": PipPackageInstallerNode
}

# Display name mappings for ComfyUI
NODE_DISPLAY_NAME_MAPPINGS = {
    "PipPackageInstaller": "Pip Package Installer"
}
