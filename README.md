# ComfyUI Wheel Installer

A custom ComfyUI node that installs Python wheels from pre-configured URLs. This node provides a dropdown widget to select and install wheels directly from your ComfyUI workflow.

## Features

- Dropdown widget populated from a configuration file
- Install Python wheels from URLs
- Force reinstall option
- Status output showing installation success/failure
- Easy configuration through a simple text file

## Installation

1. Clone or download this repository into your ComfyUI `custom_nodes` directory:

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/marduk191/comfyui_wheel_installer.git
```

2. Restart ComfyUI to load the new node.

## Configuration

Edit the `wheel_urls.txt` file in this directory to add your wheel URLs:

```txt
# ComfyUI Wheel Installer - Wheel URLs Configuration
# Add one wheel URL per line. Lines starting with # are comments.

https://example.com/packages/numpy-1.24.0-cp311-cp311-win_amd64.whl
https://example.com/packages/torch-2.0.0-cp311-cp311-linux_x86_64.whl
https://example.com/packages/pillow-9.5.0-cp311-cp311-manylinux_2_17_x86_64.whl
```

### Configuration Guidelines

- One URL per line
- Lines starting with `#` are treated as comments
- Empty lines are ignored
- URLs should point directly to `.whl` files
- The filename will be extracted and shown in the dropdown

## Usage

1. In ComfyUI, add the **Wheel Installer** node to your workflow (found under `utils` category)

2. Select a wheel from the dropdown menu

3. Toggle **force_reinstall** if you want to force reinstallation (useful for updating existing packages)

4. Run the workflow - the node will:
   - Install the selected wheel using pip
   - Output a status message
   - Return a success boolean

### Node Inputs

- **wheel_url** (dropdown): Select from configured wheel URLs
- **force_reinstall** (boolean): Force reinstallation of the package (default: No)

### Node Outputs

- **status_message** (STRING): Human-readable status message
- **success** (BOOLEAN): `True` if installation succeeded, `False` otherwise

## Example Workflow

```
[Wheel Installer Node]
  wheel_url: "https://example.com/package.whl"
  force_reinstall: No

  ↓ status_message: "Successfully installed: package.whl"
  ↓ success: True
```

## Technical Details

- Uses Python's `subprocess` module to call `pip install`
- Installation timeout: 5 minutes
- Captures both stdout and stderr
- Compatible with all Python wheel formats

## Troubleshooting

### No wheels showing in dropdown

- Check that `wheel_urls.txt` exists in the node directory
- Ensure the file has at least one non-comment, non-empty line
- Restart ComfyUI after modifying the configuration file

### Installation fails

- Verify the wheel URL is accessible
- Check that the wheel is compatible with your Python version and platform
- Review the ComfyUI console for detailed error messages
- Ensure you have write permissions for your Python environment

### Permission errors

- If running in a virtual environment, ensure it's activated
- On Linux/Mac, you may need to run ComfyUI with appropriate permissions
- Consider using user-level installs if system-level installs fail

## Security Considerations

- Only add wheel URLs from trusted sources
- Verify wheel integrity before adding to configuration
- Be cautious with force reinstall as it may downgrade packages
- Review the console output for any security warnings from pip

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Author

marduk191

## Changelog

### v1.0.0 (2025-11-21)
- Initial release
- Basic wheel installation from configured URLs
- Dropdown widget based on configuration file
- Force reinstall option
- Status and success outputs
