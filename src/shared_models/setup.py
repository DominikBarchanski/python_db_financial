from setuptools import setup, find_packages

setup(
    name='my_shared_library',  # Nazwa twojej biblioteki
    version='0.1.0',  # Wersja twojej biblioteki
    description='Opis twojej biblioteki',
    author='Twoje Imię i Nazwisko',
    author_email='twój@email.com',
    packages=find_packages(),  # Automatyczne wykrywanie pakietów w projekcie
    install_requires=[  # Lista zależności twojej biblioteki
        # Tutaj możesz wymienić inne biblioteki Pythona, które twoja biblioteka potrzebuje do działania
    ],
)
