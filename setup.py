import pathlib
import re
import setuptools


root = pathlib.Path(__file__).absolute().parent
package_path = root / 'brain_computer_interface'
readme_path = root / 'README.md'
requirements_path = root / 'requirements.txt'
github_url = 'https://github.com/sahargavriely/'
'the-unbearable-ease-of-programming'


def get_version():
    path = package_path / '__init__.py'
    text = path.read_text()
    version = re.search(r"version = '(.*?)'", text)
    if version:
        return version.group(1)
    return '-.-.-'


def get_documentation():
    return readme_path.read_text()


def get_requirements():
    return requirements_path.read_text().splitlines()


def get_package_configuration():
    config = dict(
        name = 'brain_computer_interface',
        version = get_version(),
        author = 'Sahar Gavriely',
        author_email = 'gav6sa@gmail.com',
        description = "A brain-computer-interface (BCI), a direct"
                      "communication pathway between the brain's "
                      "electrical activity and an external device, "
                      "most commonly a computer or robotic limb.",
        long_description = get_documentation(),
        long_description_content_type = 'text/markdown',
        url = github_url,
        project_urls = {
            'Documentation':
                'https://the-unbearable-ease-of-programming.'
                'readthedocs.io/en/latest/',
            'Source': github_url,
            'Tracker': f'{github_url}/issues',
        },
        packages = setuptools.find_packages(),
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
        ],
        python_requires = '>=3.8',
        install_requires = get_requirements(),
        entry_points = {
            'console_scripts': [
                'brain_computer_interface = '
                'brain_computer_interface.__main__:main',
            ],
        },
    )
    return config


if __name__ == '__main__':
    config = get_package_configuration()
    setuptools.setup(**config)
