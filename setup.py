# netbox_ping/setup.py

from setuptools import setup, find_packages

setup(
    name="netbox_ping",
    version="0.2",
    description="A NetBox plugin for pinging prefixes and IP addresses.",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
       # "Django>=4.0",
        # Add other dependencies if any
    ],
)
