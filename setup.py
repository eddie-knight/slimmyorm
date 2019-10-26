import setuptools


long_description = ("This package slims down the complexities "
                    "of mysql into a few key options that are "
                    "necessary for simple application logic.")

setuptools.setup(
    name="slimmyorm",
    version="0.0.81",
    author="Eddie Knight",
    description="Lightweight wrapper for mysql.connector",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/eddie-knight/slimmyorm",
    packages=setuptools.find_packages(),
    install_requires=[
            'mysql-connector-python',
            'pathlib'
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
