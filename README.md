# ComfyUI Wheel Installer & Pip Package Installer

<img width="943" height="344" alt="image" src="https://github.com/user-attachments/assets/e298dedb-ab20-451c-b080-059dd01ed9dd" />


Custom ComfyUI nodes for installing Python packages directly from your workflows. Includes two nodes:

1. **Wheel Installer** - Install Python wheels from pre-configured URLs
2. **Pip Package Installer** - Install pip packages by name from PyPI or other sources

## Features

- Dropdown widgets populated from configuration files
- Install Python wheels from URLs or pip packages by name
- Force reinstall and upgrade options
- Status output showing installation success/failure
- Easy configuration through simple text files

## Installation

1. Clone or download this repository into your ComfyUI `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/marduk191/comfyui_wheel_installer.git
```

2. Restart ComfyUI to load the new node.

## Configuration

### Wheel Installer Configuration

Edit the `wheel_urls.txt` file in this directory to add your wheel URLs:

```txt
# ComfyUI Wheel Installer - Wheel URLs Configuration
# Add one wheel URL per line. Lines starting with # are comments.

https://example.com/packages/numpy-1.24.0-cp311-cp311-win_amd64.whl
https://example.com/packages/torch-2.0.0-cp311-cp311-linux_x86_64.whl
https://example.com/packages/pillow-9.5.0-cp311-cp311-manylinux_2_17_x86_64.whl
```

**Configuration Guidelines:**
- One URL per line
- Lines starting with `#` are treated as comments
- Empty lines are ignored
- URLs should point directly to `.whl` files
- The filename will be extracted and shown in the dropdown

### Pip Package Installer Configuration

Edit the `package_names.txt` file in this directory to add package names:

```txt
# ComfyUI Pip Package Installer - Package Names Configuration
# Add one package name per line. Lines starting with # are comments.
# You can specify versions using standard pip syntax.
# You can also include multiple packages and pip flags on a single line.

# Single package examples:
numpy==1.24.0
pillow>=9.0.0
requests

# Multiple packages on one line:
torch torchvision torchaudio

# Custom index URL (for PyTorch with CUDA):
torch torchvision --index-url https://download.pytorch.org/whl/cu130
```

**Configuration Guidelines:**
- One entry per line (can be a single package or multiple packages with flags)
- Lines starting with `#` are treated as comments
- Empty lines are ignored
- Use standard pip package naming (supports version specifiers like `==`, `>=`, `~=`)
- **Multiple packages and pip flags are supported on a single line**
- Common flags: `--index-url`, `--extra-index-url`, `--no-cache-dir`, `--no-deps`
- Packages will be installed from PyPI unless otherwise configured with `--index-url`

## Usage

### Wheel Installer Node

1. In ComfyUI, add the **Wheel Installer** node to your workflow (found under `utils` category)
2. Select a wheel from the dropdown menu
3. Toggle **force_reinstall** if you want to force reinstallation (useful for updating existing packages)
4. Run the workflow - the node will install the selected wheel and output status

**Node Inputs:**
- **wheel_url** (dropdown): Select from configured wheel URLs
- **force_reinstall** (boolean): Force reinstallation of the package (default: No)

**Node Outputs:**
- **status_message** (STRING): Human-readable status message
- **success** (BOOLEAN): `True` if installation succeeded, `False` otherwise

### Pip Package Installer Node

1. In ComfyUI, add the **Pip Package Installer** node to your workflow (found under `utils` category)
2. Select a package from the dropdown menu
3. Toggle **force_reinstall** to force reinstallation (replaces existing installation)
4. Toggle **upgrade** to upgrade the package if already installed
5. Run the workflow - the node will install the selected package and output status

**Node Inputs:**
- **package_name** (dropdown): Select from configured package names
- **force_reinstall** (boolean): Force reinstallation of the package (default: No)
- **upgrade** (boolean): Upgrade the package to the latest version (default: No)

**Node Outputs:**
- **status_message** (STRING): Human-readable status message
- **success** (BOOLEAN): `True` if installation succeeded, `False` otherwise

## Example Workflows

### Wheel Installer Example
```
[Wheel Installer Node]
  wheel_url: "https://example.com/package.whl"
  force_reinstall: No

  ↓ status_message: "Successfully installed: package.whl"
  ↓ success: True
```

### Pip Package Installer Example
```
[Pip Package Installer Node]
  package_name: "torch torchvision --index-url https://download.pytorch.org/whl/cu130"
  force_reinstall: No
  upgrade: No

  ↓ status_message: "Successfully installed: torch torchvision --index-url https://download.pytorch.org/whl/cu130"
  ↓ success: True
```

## Technical Details

**Wheel Installer:**
- Uses Python's `subprocess` module to call `pip install`
- Installation timeout: 5 minutes
- Captures both stdout and stderr
- Compatible with all Python wheel formats

**Pip Package Installer:**
- Uses Python's `subprocess` module to call `pip install`
- Installation timeout: 10 minutes (larger packages may take longer)
- Captures both stdout and stderr
- Supports all pip package naming conventions
- Compatible with version specifiers (`==`, `>=`, `<=`, `~=`, etc.)
- **Supports multiple packages and pip flags in a single entry** (uses `shlex` for proper argument parsing)
- Can pass custom index URLs, extra index URLs, and other pip options

## Troubleshooting

### No items showing in dropdown

**For Wheel Installer:**
- Check that `wheel_urls.txt` exists in the node directory
- Ensure the file has at least one non-comment, non-empty line
- Restart ComfyUI after modifying the configuration file

**For Pip Package Installer:**
- Check that `package_names.txt` exists in the node directory
- Ensure the file has at least one non-comment, non-empty line
- Restart ComfyUI after modifying the configuration file

### Installation fails

**For Wheel Installer:**
- Verify the wheel URL is accessible
- Check that the wheel is compatible with your Python version and platform
- Review the ComfyUI console for detailed error messages
- Ensure you have write permissions for your Python environment

**For Pip Package Installer:**
- Verify the package name is correct (check PyPI if unsure)
- Check for typos in version specifiers
- Review the ComfyUI console for detailed error messages
- Ensure you have internet connectivity (for PyPI packages)
- Verify write permissions for your Python environment

### Permission errors

- If running in a virtual environment, ensure it's activated
- On Linux/Mac, you may need to run ComfyUI with appropriate permissions
- Consider using user-level installs if system-level installs fail

### Conflicts between force_reinstall and upgrade

- **force_reinstall**: Completely removes and reinstalls the exact version specified
- **upgrade**: Updates to the latest available version (or version specified)
- Using both together may cause unexpected behavior - choose one option based on your needs

## Security Considerations

**General:**
- Always review the console output for any security warnings from pip
- Be cautious with force reinstall as it may downgrade packages
- Only install packages in trusted environments

**Wheel Installer:**
- Only add wheel URLs from trusted sources
- Verify wheel integrity before adding to configuration
- Ensure URLs use HTTPS when possible

**Pip Package Installer:**
- Only add package names from trusted sources (verify on PyPI)
- Be aware that packages can execute code during installation
- Review package dependencies before installation
- Consider pinning versions for reproducibility and security

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

marduk191

## Changelog

### v1.1.1 (2025-11-21)
- **Fixed**: Pip Package Installer now properly handles multiple packages and pip flags
- Support for custom index URLs (e.g., `--index-url https://download.pytorch.org/whl/cu130`)
- Support for multiple packages on one line (e.g., `torch torchvision torchaudio`)
- Uses `shlex` for proper argument parsing with quoted strings
- Updated configuration examples and documentation

### v1.1.0 (2025-11-21)
- Added Pip Package Installer node
- Install packages by name from PyPI
- Added upgrade option for Pip Package Installer
- Extended timeout for pip packages (10 minutes)
- Updated documentation for both nodes

### v1.0.0 (2025-11-21)
- Initial release
- Wheel Installer node
- Basic wheel installation from configured URLs
- Dropdown widget based on configuration file
- Force reinstall option
- Status and success outputs
