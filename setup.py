from setuptools import setup, find_packages

setup(
    name="diabetes-prediction",
    version="1.0.0",
    python_requires='>=3.10,<3.11',  # Explicitly require Python 3.10
    packages=find_packages(),
    install_requires=[
        'streamlit>=1.32.0,<2.0.0',
        'pandas>=2.1.0,<3.0.0',
        'numpy>=1.24.0,<2.0.0',
        'scikit-learn>=1.3.0,<2.0.0',
        'matplotlib>=3.7.0,<4.0.0',
        'seaborn>=0.12.0,<0.14.0',
        'python-dotenv>=1.0.0,<2.0.0',
        'Pillow>=10.0.0,<11.0.0',
        'pydeck>=0.8.0,<1.0.0',
        'protobuf>=4.0.0,<5.0.0'
    ]
)
