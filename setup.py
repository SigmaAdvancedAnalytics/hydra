from distutils.core import setup

setup(name='hydra',
	version='0.1',
	description='Multi-headed connector for rapid data extraction from new environments',
	author='Joshua Barber',
	url='https://github.com/joshua-barber/hydra.git',
	py_modules=['tableau_connector','lotus_connector','SQL_connector','results_generator','uploader'],
)