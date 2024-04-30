from setuptools import setup

setup(
    name='cloudflare-dynamic-dns-client',
		description='Allows selfhosting on cloudflare with a dynamic ip address',
    version='0.1.2',
    packages=['cloudflare_dynamic_dns'],
		author="Littlewhinging",
    install_requires=[
      "cloudflare==2.11.1",
			"Requests==2.31.0"
    ],
		entry_points={
			'console_scripts': [
				'cloudflare-dynamic-dns = cloudflare_dynamic_dns.__main__:main'
			],
    }
)