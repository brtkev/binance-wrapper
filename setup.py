from setuptools import setup

setup(
   name='binanceWrapper',
    version='1.0.2',    
    description='a wrapper for binance exchange API',
    url='https://github.com/brtkev/binance-wrapper',
    author='Kevin Breto',
    author_email='kbreto2911@gmail.com',
    license='MIT',
    packages=['binanceWrapper'],
    install_requires=['requests==2.26.0'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Trading/Wrapper',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux :: Windows',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
