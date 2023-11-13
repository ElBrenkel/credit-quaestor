import setuptools

setuptools.setup(
    include_package_data=True,
    name="CreditQuaestor",
    version="0.0.1",
    description="very portant",
    author="Moustachio",
    packages=setuptools.find_packages(),
    install_requires=[
        "botogram2==0.6.1",
        "python-dotenv==1.0.0",
        "pymongo==4.6.0",
        "marshmallow==3.20.1",
    ],
)
