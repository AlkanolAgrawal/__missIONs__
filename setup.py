from setuptools import setup, find_packages

def get_requireds(file_path):
    with open(file_path) as f:
        lst = f.readlines()
        lstn=[]
        for x in lst:
            a=x.strip()
            if a == "":
                continue
            if "-e ." == a:
                continue
            else:
                lstn.append(a)
    return lstn
setup(
    name='First_Mission',
    version='0.0.1',
    author='Alkanol',
    author_email='coding.alkanol@gmail.com',
    packages=find_packages(),
    install_requires=get_requireds('requirements.txt'),
    
)