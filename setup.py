from setuptools import setup, find_packages

# Core dependencies
INSTALL_REQUIRES = [
    'streamlit==1.32.0',
    'pandas==2.1.4',
    'numpy==1.26.3',
    'scikit-learn==1.3.2',
    'matplotlib==3.8.2',
    'seaborn==0.13.2',
    'joblib==1.3.2',
    'python-dotenv==1.0.0',
    'Pillow==10.4.0',
    'pydeck==0.9.1',
    'protobuf==4.25.8',
    'typing-extensions==4.10.0'
]

setup(
    name="diabetes-prediction",
    version="1.0.0",
    python_requires='>=3.10,<3.11',
    packages=find_packages(),
    install_requires=INSTALL_REQUIRES,
    # Include package data files (like .csv files)
    include_package_data=True,
    package_data={
        '': ['*.csv'],
    },
    # Metadata
    author="Your Name",
    author_email="your.email@example.com",
    description="A Streamlit app for diabetes prediction",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/diabetes-prediction",
)
