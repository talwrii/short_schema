import setuptools.command.test
import os

HERE = os.path.dirname(__file__)

class ToxTest(setuptools.command.test.test):
    user_options = []

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)

    def run_tests(self):
        import tox
        tox.cmdline()
        tox.cmdline(['-c', 'tox.ini'])


setuptools.setup(
    name='short_schema',
    version="0.1.1",
    author='Tal Wrii',
    author_email='talwrii@gmail.com',
    description='',
    license='GPLv3',
    keywords='',
    url='',
    packages=['short_schema'],
    long_description='See https://github.com/talwrii/short_schema',
    entry_points={
        'console_scripts': ['short_schema=short_schema.short_schema:main']
    },
    classifiers=[
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ],
    install_requires=['genson'],
    cmdclass = {'test': ToxTest},
)
