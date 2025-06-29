from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="diabetes_prediction",
    version="1.0.0",
    python_requires='>=3.10,<3.11',  # Strictly Python 3.10.x
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    package_data={
        '': ['*.csv', '*.toml'],
    },
    entry_points={
        'console_scripts': [
            'diabetes-prediction=app:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Streamlit app for diabetes prediction",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/diabetes-prediction",
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
