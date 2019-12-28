import setuptools

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name="vkbottle",
    version="1.33",
    author="timoniq",
    description="Working with VK by this homogenetic way and it's awesome!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='GPL-3.0',
    url="https://github.com/timoniq/vkbottle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=["aiohttp", "pydantic", "colorama", "termcolor", "vbml"],
)
