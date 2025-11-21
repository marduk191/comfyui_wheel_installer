"""
ComfyUI Wheel Installer and Pip Package Installer Nodes
Custom nodes for installing Python wheels and pip packages.
"""

from .wheel_installer_node import NODE_CLASS_MAPPINGS as WHEEL_NODE_CLASS_MAPPINGS
from .wheel_installer_node import NODE_DISPLAY_NAME_MAPPINGS as WHEEL_NODE_DISPLAY_NAME_MAPPINGS
from .pip_package_installer_node import NODE_CLASS_MAPPINGS as PIP_NODE_CLASS_MAPPINGS
from .pip_package_installer_node import NODE_DISPLAY_NAME_MAPPINGS as PIP_NODE_DISPLAY_NAME_MAPPINGS

# Merge the mappings from both nodes
NODE_CLASS_MAPPINGS = {
    **WHEEL_NODE_CLASS_MAPPINGS,
    **PIP_NODE_CLASS_MAPPINGS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **WHEEL_NODE_DISPLAY_NAME_MAPPINGS,
    **PIP_NODE_DISPLAY_NAME_MAPPINGS
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
