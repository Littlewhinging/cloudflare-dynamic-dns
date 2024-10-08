from setuptools import setup

try:
	with open("readme.md","r") as f:
		description = f.read()
except:
	description = 'Allows selfhosting on cloudflare with a dynamic ip address'

setup(
	name='cloudflare-dynamic-dns-client',
	description='Allows selfhosting on cloudflare with a dynamic ip address',
	long_description=description,
	long_description_content_type='text/markdown',
	version='0.2.3',
	license='MIT',
	url='https://github.com/Littlewhinging/cloudflare-dynamic-dns',
	packages=['cloudflare_dynamic_dns'],
	author="Littlewhinging",
	install_requires=[
		"cloudflare==2.11.1",
		"requests==2.32.0"
	],
	entry_points={
		'console_scripts': [
			'cloudflare-dynamic-dns = cloudflare_dynamic_dns.__main__:main'
		],
	}
)
