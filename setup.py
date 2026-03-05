from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="croc-ui",
    version="1.0.0",
    author="Swarup Kumar Sahoo",
    author_email="",
    description="A Python library for building beautiful static websites using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swarup-kumar-sahoo/croc",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["html", "css", "web", "ui", "static-site", "croc"],
    project_urls={
        "Bug Reports": "https://github.com/swarup-kumar-sahoo/croc/issues",
        "Source": "https://github.com/swarup-kumar-sahoo/croc",
    },
)
