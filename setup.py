from setuptools import setup
import glob

setup(
    name='starry_maps',
    version='0.0.3',
    author='Rodrigo Luger',
    author_email='rodluger@gmail.com',
    url='https://github.com/rodluger/starry_maps',
    description='Surface maps for starry.',
    long_description='',
    license='GPL',
    packages=['starry_maps'],
    install_requires=['numpy',
                      'matplotlib',
                      'healpy',
                      'Pillow'],
    zip_safe=False,
    data_files=[('starry_maps', glob.glob('starry_maps/*.jpg'))]
)
