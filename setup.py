from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gitignore-gen",
    version="0.1.1",
    author="Naymul Islam",
    author_email="naymul504@gmail.com",
    description="A tool to generate .gitignore files for various languages and frameworks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['gitignore-gen=gitignore_gen.main:main'],
    },
    install_requires=[
        'requests',
    ]

)
