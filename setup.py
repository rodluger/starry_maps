from setuptools import setup
import glob
import platform

install_requires = ['numpy', 'matplotlib', 'scipy', 'Pillow']
if platform.system() != "Windows":
    install_requires.append('healpy')

setup(
    name='starry_maps',
    version='0.0.11',
    author='Rodrigo Luger',
    author_email='rodluger@gmail.com',
    url='https://github.com/rodluger/starry_maps',
    description='Surface maps for starry.',
    long_description='',
    license='GPL',
    packages=['starry_maps'],
    install_requires=install_requires,
    zip_safe=False,
    data_files=[('starry_maps', glob.glob('starry_maps/*.jpg'))],
    include_package_data=True
)
