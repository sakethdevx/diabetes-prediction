from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="diabetes_prediction",
    version="1.0.0",
    python_requires='>=3.10',  # More flexible Python version requirement
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
    package_data={
        '': ['*.csv', '*.toml', '*.joblib'],
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
    url="https://github.com/saketh-005/diabetes-prediction",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
