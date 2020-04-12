from setuptools import setup,find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='geoedfframework',
      version='0.1',
      description='GeoEDF Connector Processor Framework',
      url='http://github.com/geoedf/framework',
      author='Rajesh Kalyanam',
      author_email='rkalyanapurdue@gmail.com',
      license='MIT',
      python_requires='~=3.6',
      packages=find_packages(),
      scripts=['bin/run-connector-plugin.py','bin/run-processor-plugin.py','bin/merge.py','bin/collect.py'],
      install_requires=['pyyaml','regex'],
      include_package_data=True,
      zip_safe=False)
