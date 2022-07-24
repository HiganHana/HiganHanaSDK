from distutils.core  import setup


setup(
    name="higanhana_sdk",
    version="0.0.1",
    author="higanhana server devs",
    description="higanhana server SDK",
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HiganHana/HiganHanaSDK",
    packages=[
        
    ],
    install_requires=[
        "flask",
        "flask-sqlalchemy",
        "sqlalchemy",
        "genshin"
    ]
)