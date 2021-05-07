import setuptools

setuptools.setup(
    name='rhasspy_datetime',
    author='Daenara',
    version='0.0.3',
    url='https://github.com/Daenara/rhasspy_datetime',
    packages=setuptools.find_packages(),
    py_modules=["rhasspy_datetime", "data_types", "languages"],
    python_requires='>=3.7, <3.9',
    install_requires=["pytz"],
    package_data={
        '': ['config.default'],
    }
)
