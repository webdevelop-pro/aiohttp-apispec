from setuptools import find_packages, setup


def read(file_name):
    with open(file_name, encoding="utf-8") as fp:
        content = fp.read()
    return content


setup(
    name='aiohttp-apispec',
    version='3.1.0',
    description='Build and document REST APIs with aiohttp and apispec',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author='Danilchenko Maksim',
    author_email='dmax.dev@gmail.com',
    packages=find_packages(exclude=('test*',)),
    package_dir={'aiohttp_apispec': 'aiohttp_apispec'},
    include_package_data=False,
    package_data={'aiohttp_apispec': ['static/*']},
    install_requires=read('requirements.txt').split(),
    license='MIT',
    url='https://github.com/webdevelop-pro/aiohttp-apispec',
    zip_safe=False,
    keywords='aiohttp marshmallow apispec swagger',
    python_requires='>=3.9',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
)
