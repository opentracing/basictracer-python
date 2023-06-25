from setuptools import setup

setup(
    name='basictracer',
    version='3.2.1.dev0',
    author='The OpenTracing Authors',
    author_email='info@opentracing.io',
    license='MIT',
    url='https://github.com/opentracing/basictracer-python',
    keywords=['basictracer', 'opentracing'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['basictracer'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'protobuf>=3.0.0b2.post2',
        'opentracing>=2.0,<3.0',
        'six>=1.10.0,<2.0',
    ],
    extras_require={
        'tests': [
            'flake8',
            'flake8-quotes',
            'pytest',
            'pytest-cov',
            'Sphinx',
            'sphinx_rtd_theme'
        ]
    },
)
