from setuptools import setup, find_packages

setup(
    name="slaviclean",
    version="0.0.4",
    description="Text filter designed to cleanse text of profanity and offensive language, specifically tailored for Ukrainian, Russian, and Surzhik.",
    author="Tetiana Lytvynenko",
    author_email="lytvynenkotv@gmail.com",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=[
        "nlp tools", "natural language processing",
        "text processing", "linguistic tools", "profanity filter",
        "obscene filter", "slavic languages", "slavic profanity filter",
        "slavic text cleaner", "text sanitization"
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.2.3,<2.3",
        "flexi-nlp-tools>=0.5.5, <0.6",
        "spacy>=3.8.4, <3.9",
        "pymorphy3>=2.0, <2.1",
        "pymorphy3-dicts-uk>=2.4, <2.5"
    ],
    python_requires=">=3.11",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    package_data={
        "slaviclean.resources": ["*.csv"],
        "slaviclean.resources.profanity": ["*.csv"],
    },
)
