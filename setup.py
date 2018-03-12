from setuptools import setup
import versioneer


if __name__ == "__main__":
    setup(
        name="ipython-adbcompleter",
        version=versioneer.get_version(),
        cmdclass=versioneer.get_cmdclass(),
        description="IPython completer for adb commands",
        long_description=open("README.md").read(),
        author="Dror Speiser",
        url="https://github.com/drorspei/ipython-adbcompleter",
        license="MIT",
        classifiers=[
            "Development Status :: 1 - Beta",
            "Framework :: IPython",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
        ],
        py_modules=["ipython_adbcompleter"],
        python_requires=">=2.7.10",
        install_requires=["ipython>=4.0"],
    )
