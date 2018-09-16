from setuptools import find_packages, setup

# to include static files and other templates, include_package_data flag also needs a MANIFEST.in
setup(
    name='flaskr',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
