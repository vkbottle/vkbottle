import setuptools

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except UnicodeDecodeError:
    with open("README.md", "r") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ""

with open("vkbottle/const.py") as f:
    exec(f.read())

setuptools.setup(
    name="vkbottle",
    version=locals()["__version__"],
    author="timoniq",
    description="Homogenic!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/timoniq/vkbottle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp", "pydantic", "contextvars", "vbml==0.5.93", "watchgod", "loguru"],
)
