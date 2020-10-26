import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dictparse",
    version="1.3",
    packages=setuptools.find_packages(),
    author="Julian Nash",
    author_email="julianjamesnash@gmail.com",
    description="A Python dictionary parser",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords="dict dictionary parser flask django validation request json",
    url="https://github.com/Julian-Nash/dictparse",
    project_urls={
        "Bug Tracker": "https://github.com/Julian-Nash/dictparse",
        "Documentation": "https://github.com/Julian-Nash/dictparse",
        "Source Code": "https://github.com/Julian-Nash/dictparse",
    },
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)