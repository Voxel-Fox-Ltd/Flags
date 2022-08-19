from setuptools import setup


requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()


version: str = '0.1.0'


readme = ''
with open('README.rst') as f:
    readme = f.read()


extras_require = {
}


packages = [
    'flags',
]


setup(
    name='flags',
    author='Kae Bartlett',
    url='https://github.com/Voxel-Fox-Ltd/Flags',
    project_urls={
        # "Documentation": "https://novus.readthedocs.io/en/latest/",
        "Issue tracker": "https://github.com/Voxel-Fox-Ltd/Flags/issues",
    },
    version=version,
    packages=packages,
    license='GPL',
    description='A wrapper for easily making bitwise flags.',
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires='>=3.6.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Typing :: Typed',
    ],
)
