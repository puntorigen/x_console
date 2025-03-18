from setuptools import setup, find_packages

setup(
    name='x_console',
    version='0.1.1',
    packages=find_packages(),
    package_dir={'': 'x_console'},
    entry_points={},
    author='Pablo Schaffner',
    author_email='pablo@puntorigen.com',
    description='Class for nice and easy user interaction, with coloring and automatic translation support',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://github.com/puntorigen/x_console',
    install_requires=[
        'rich',
        'rich_click',
        'simple_term_menu',
        'yaspin',
        'polib'
    ],
    extras_require={
        'online': ['lingua-language-detector','deep_translator'],
        'offline': ['lingua-language-detector','easynmt'],
        'full': ['lingua-language-detector','deep_translator','easynmt']
    },
    python_requires='>=3.7, <4',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
