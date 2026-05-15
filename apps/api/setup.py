"""Setup configuration for Thai Food Image Classification API."""
from setuptools import setup, find_packages

setup(
    name="thai-food-image-classification-api",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask==2.0.0",
        "Flask-Cors==3.0.10",
        "keras==2.11.0",
        "keras-nightly==2.5.0.dev2021032900",
        "Keras-Preprocessing==1.1.2",
        "numpy==1.23.5",
        "pymongo==4.3.3",
        "python-dotenv==0.21.0",
        "requests==2.26.0",
        "tensorflow==2.11.0",
        "pillow==9.3.0",
    ],
    extras_require={
        "dev": [
            "pytest==7.4.3",
            "pytest-cov==4.1.0",
            "pytest-mock==3.12.0",
            "pytest-flask==1.3.0",
            "black==23.12.1",
            "flake8==7.0.0",
            "mypy==1.8.0",
        ]
    },
    python_requires=">=3.8",
)
