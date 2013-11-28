from setuptools import setup, find_packages

setup(
    name='sveedocuments',
    version=__import__('sveedocuments').__version__,
    description=__import__('sveedocuments').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='http://pypi.python.org/pypi/sveedocuments',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Development Status :: 5 - Production/Stable",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Text Processing :: Markup',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'docutils>=0.7',
        'rstview',
        'autobreadcrumbs',
        'djangocodemirror',
        'django-mptt>=0.5.2',
        'crispy-forms-foundation>=0.2.3',
        'django-braces>=0.2.1',
    ],
    include_package_data=True,
    zip_safe=False
)