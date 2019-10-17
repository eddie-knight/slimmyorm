import setuptools

setuptools.setup(
    name="slimmyorm",
    version="0.0.4",
    author="Eddie Knight",
    description="Lightweight wrapper for mysql.connector",
    long_description_content_type="text/markdown",
    url="https://https://github.com/eddie-knight/slimmyorm",
    packages=setuptools.find_packages(),
    install_requires=[
            'mysql-connector-python',
        ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
