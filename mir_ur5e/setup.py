from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup
d = generate_distutils_setup(
    packages=['mir_ur5e'],
    package_dir={'': 'src'}
)
setup(**d)