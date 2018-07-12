from setuptools import setup, find_packages


version = '0.2.1'


setup(
    name='qthmi.ads',
    version=version,
    description='',
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='',
    author='',
    author_email='',
    url='',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['qthmi'],
    include_package_data=True,
    test_suite='nose.collector',
    test_requires=['Nose'],
    zip_safe=False,
    install_requires=[
        'setuptools',
        'matplotlib',
        'qthmi.main==0.2.1',
    ],
    dependency_links=[
        "git+https://github.com/stlehmann/qthmi.main.git#egg=qthmi.main-0.2.1",
    ]
)
