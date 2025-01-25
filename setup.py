from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='netbox_ping',
    version='0.2',
    description='Ping IPs and subnets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Christian Rose',
    license='GPL-3.0',
    packages=["netbox_ping"],
    package_data={"netbox_ping": ["templates/netbox_ping/*.html"]},
    zip_safe=False
    )