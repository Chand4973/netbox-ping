from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='netbox_ping',
    version='4.1.5',
    description='Syncing existing interfaces with the interfaces from a device type template in NetBox 4+',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Keith Knowles',
    author_email='mkknowles@outlook.com',
    license='GPL-3.0',
    packages=["netbox_ping"],
    package_data={"netbox_ping": ["templates/netbox_ping/*.html"]},
    zip_safe=False
    )