from setuptools import setup

setup(
    name='displacy_service',
    version='0.1',
    description='REST microservice for Explosion AI\'s interactive demos ' +
                'and visualisers.',
    author='explosion.ai & Johannes Gontrum',
    author_email='gontrum@me.com',
    include_package_data=True,
    license='MIT',
    entry_points={
          'console_scripts': [
              'download_models = displacy_service.scripts.download:download_models',
              'run_server = displacy_service.scripts.app:run'
          ]
      }
)
