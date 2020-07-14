import setuptools

# readme.md = github readme.md, 這裡可接受markdown寫法
# 如果沒有的話，需要自己打出介紹此專案的檔案，再讓程式知道

with open("Discription.md", "r",encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VerdictCut", # 
    version='0.1.0',
    author="seanbbear",
    author_email="k7489759@gmail.com",
    description="cut the verdict into different part",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seanbbear/VerdictCut",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)