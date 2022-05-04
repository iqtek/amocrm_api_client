from setuptools import setup
from setuptools import find_packages


install_requires = [
    'aiohttp==3.8.1',
    'aioredis==2.0.0',
    'aiosignal==1.2.0',
    'async-timeout==4.0.1',
    'attrs==21.2.0',
    'charset-normalizer==2.0.9',
    'frozenlist==1.2.0',
    'idna==3.3',
    'multidict==5.2.0',
    'pydantic==1.8.2',
    'pydantic-collections==0.2.0',
    'PyYAML==6.0',
    'typing_extensions==4.0.1',
    'ujson==4.3.0',
    'yarl==1.7.2',
    'PyJWT~=2.3.0',
    'aiofile~=3.7.3',
]


prod_requires = [
    *install_requires,
]


dev_requires = [
    *prod_requires,
    "mypy",
    "flake8",
]


test_requires = [
    *dev_requires,
    "pytest~=6.2.5",
    "pytest-runner",
]


docs_requires = [
    "Sphinx",
    "sphinx-autobuild",
]


setup(
    name="amo_crm_api_client",
    description="Api Client for AmoCrm.",
    version="2.0.0",
    license="MIT",
    packages=find_packages(exclude=[
        'build',
        'data',
        'dist',
        'requirements',
        'contrib',
        'docs',
        'tests',
        'logs']
    ),
    status='Production',
    install_requires=install_requires,
    extras_require={
        "prod": prod_requires,
        "dev": dev_requires,
        "test": test_requires,
        "docs": docs_requires,
    },
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
