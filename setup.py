from setuptools import setup

setup(
    name='basictracer',
    version='1.0rc1',
    author='Brandon Gonzalez, The OpenTracing Authors',
    author_email='bg@lightstep.com',
    license='MIT',
    url='https://github.com/opentracing/basictracer-python',
    keywords=['basictracer', 'opentracing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['basictracer'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'futures',
        'protobuf>=3.0.0b2.post2',
        'opentracing>=1.0rc3'
    ],
    extras_require={
        'tests': [
            'doubles',
            'flake8',
            'flake8-quotes',
            'mock<1.1.0',
            'pytest>=2.7,<3',
            'pytest-cov',
            'pytest-mock',
            'Sphinx',
            'sphinx_rtd_theme'
        ]
    },
)
