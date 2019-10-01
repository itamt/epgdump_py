from setuptools import setup

PACKAGE_NAME = 'epgdump_py'

setup(
    # metadata
    name=PACKAGE_NAME,
    version='1.0.0',

    # options
    packages=[PACKAGE_NAME],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'dev': [],
    },
    entry_points='''
        [console_scripts]
        {app}={pkg}.cli:main
    '''.format(app=PACKAGE_NAME.replace('_', '-'), pkg=PACKAGE_NAME),
)
