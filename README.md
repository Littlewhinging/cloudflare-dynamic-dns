# Cloudflare Dynamic DNS

Cloudflare Dynamic DNS is a Python package designed to automate the process of updating Cloudflare A records whenever your server's IP address changes. This can be particularly useful for users with dynamic IP addresses, ensuring that your domain always points to the correct server.

## Features

- Automatically updates Cloudflare A records when your server's IP address changes.
- Interface to guide you through the setup process.
- Select multiple records you want the server to update.
- Continuously monitors for IP changes and updates Cloudflare accordingly.

## Installation

You can install Cloudflare Dynamic DNS via pip:

```bash
pip install cloudflare-dynamic-dns-client
```

## Usage

To use Cloudflare Dynamic DNS, follow these steps:

**Configuration**: Running `cloudflare-dynamic-dns` for the first time will allow you to enter an API key and select the records you want to update.

**Running**: Once configured, running `cloudflare-dynamic-dns` again will resume monitoring for ip changes and updating cloudflare records.

**Editing Configuration**: Running `cloudflare-dynamic-dns config` will allow you to repeat to configuration step.

**Logs** Running `cloudflare-dynamic-dns logs` will output the directory containing the latest log files.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.