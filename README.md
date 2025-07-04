# NetBox Ping Plugin

![Python](https://img.shields.io/badge/python-3.12.3-blue.svg)
![NetBox](https://img.shields.io/badge/netbox-4.2.2-blue.svg)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

A NetBox plugin for pinging and discovering IPs in your network.

## Features

- Ping IPs and subnets directly from NetBox
- Auto-discover new IPs
- Track IP status with custom fields and tags
- Bulk scan operations
- Dark mode compatible UI

## Installation

```bash
pip install netbox-ping
```

## Configuration

Add to your `configuration.py`:

```python
PLUGINS = ['netbox_ping']

PLUGINS_CONFIG = {
    'netbox_ping': {
        'coming_soon': True
    }
}
```

## Usage

1. Install the plugin
2. Navigate to Plugins > NetBox Ping
3. Click "Create Required Fields & Tags"
4. Start scanning your networks!

## Requirements

- NetBox 4.0 or later
- Python 3.8 or later
- `ping` command available on the system

## Installation

### Package Installation

1. Install the package from your NetBox installation path:
   ```bash
   source /opt/netbox/venv/bin/activate
   cd /opt/netbox
   pip install git+https://github.com/DenDanskeMine/netbox-prefix-pinger.git
   ```

### Enable the Plugin

2. Add the plugin to `PLUGINS` in `/opt/netbox/netbox/netbox/configuration.py`:
   ```python
   PLUGINS = [
       'netbox_ping',
   ]
   ```

### Run Migrations

3. Apply database migrations:
   ```bash
   cd /opt/netbox
   python3 manage.py migrate
   ```

### Collect Static Files

4. Collect static files:
   ```bash
   python3 manage.py collectstatic
   ```

### Restart NetBox

5. Restart the NetBox service:
   ```bash
   sudo systemctl restart netbox
   ```

## Usage

1. Navigate to the "Plugins" menu in NetBox
2. Select "IP Pinger" from the NetBox Ping dropdown
3. You'll see the IP search interface and prefix list
4. Two actions are available for each prefix:
   - **Check Status**: Checks all existing IPs in the prefix
   - **Scan Subnet**: Discovers and adds new active IPs

### Status Indicators

- 🟢 Online Tag: IP is responding to ping
- 🔴 Offline Tag: IP is not responding
- Custom Field "Up_Down": Boolean indicator of IP status

## Configuration

No additional configuration is required. The plugin will automatically:

- Create required custom fields
- Create online/offline tags
- Set up necessary permissions

## Permissions

Users need the following permissions to use the plugin:

- `ipam.view_prefix`
- `ipam.view_ipaddress`

## Development

To set up a development environment:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/netbox-ping.git
   cd netbox-ping
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .
   ```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you have any questions or need help, please:

1. Open an issue on GitHub
2. Check existing issues for answers
3. Contact the maintainer

## Acknowledgments

- Built for NetBox (https://github.com/netbox-community/netbox)
- Inspired by the need for simple IP status tracking, this is my first plugin for NetBox.
- I'm not a good python developer, so this is probably not the best way to do this.
- The plugin `netbox-interface-synchronization` gave me a lot of inspiration, code wise, as the offical NetBox development repo had some issues, i couldn't get around.
- The plugin [netbox-interface-synchronization](https://github.com/NetTech2001/netbox-interface-synchronization/tree/main) is a great plugin, and i recommend using it if you need to synchronize interfaces.
