from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="book-converter",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool to convert PDF files to various formats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/book-converter",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
    ],
    python_requires=">=3.7",
    install_requires=[
        "PyMuPDF>=1.19.0",  # For PDF parsing
        "ebooklib>=0.17.1",  # For EPUB creation
        "python-docx>=0.8.11",  # For DOCX creation
        "markdown>=3.3.4",  # For Markdown creation
        "pillow>=8.2.0",  # For image processing
        "beautifulsoup4>=4.9.3",  # For HTML processing
        "lxml>=4.6.3",  # For XML/HTML processing
        "tqdm>=4.61.0",  # For progress bars
        "click>=8.0.1",  # For CLI
    ],
    entry_points={
        "console_scripts": [
            "book-converter=book_converter.cli:main",
        ],
    },
)
