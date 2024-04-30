from setuptools import setup

setup(
    name='cloudflare-dynamic-dns',
    version='0.1.0',
    packages=['cloudflare_dynamic_dns'],
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