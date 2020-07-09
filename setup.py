import setuptools

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except:
    with open("README.md", "r") as f:
        long_description = f.read()

setuptools.setup(
    name="vkbottle",
    version="2.7.6",
    author="timoniq",
    description="Homogenic!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPL-3.0",
    url="https://github.com/timoniq/vkbottle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp", "pydantic", "contextvars", "vbml", "watchgod",],
)
