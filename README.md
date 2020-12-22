# yepc

[![Travis branch](https://img.shields.io/travis/com/1995parham/yepc/master.svg?style=flat-square)](https://travis-ci.com/1995parham/yepc)

## Introduction

Another compiler project, nothing else. every year students of
Amirkabir University of Technology write a simple compiler and
nothing change, we are just two of them.

-- Fall 2016, Prof. Razzazi Compiler Course

## How To Run

### Backend
The backend is the core of the project that parses the grammer and generates C code.

```
python3 -mpip pipenv
pipenv install
pipenv shell
./yepc-serve.py
```

### Frontend
We have planty of time, so we have created the an Angular Frontend for our project.
The frontend project is outdated but with the help from [here](https://stackoverflow.com/questions/55921442/how-to-fix-referenceerror-primordials-is-not-defined-in-node),
it works now.

```sh
cd yepc-UI
npm install
npx bower install
npx grunt
```

## Contributors

- [Parham Alvani](https://github.com/1995parham)
- [Saman Fekri](https://github.com/samanfekri)
