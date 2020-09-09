import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dictparser",
    version="0.1",
    packages=setuptools.find_packages(),
    author="Julian Nash",
    author_email="julianjamesnash@gmail.com",
    description="A parser for incoming data",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="flask http request parser json rest",
    url="https://github.com/Julian-Nash/requestparser",
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Nash/requestparser",
        "Documentation": "https://github.com/Julian-Nash/requestparser",
        "Source Code": "https://github.com/Julian-Nash/requestparser",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)