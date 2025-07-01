# README for `interpolate` package (v0.1)

This README provides an overview of how to use the `interpolate` package, as well as some elaboration on software design choices and potential enhancements.

The `interpolate` package provides functionality to interpolate missing values within a two-dimensional matrix stored as a comma-separated (CSV) file. This version of the package only supports calculation of interpolated values by averaging all non-diagonal neighboring values in the matrix.

# Getting started

Package building and installation have only been tested in a unix-like environment (macOS Sonoma 14.6.1). Future versions will have the package and necessary dependencies installed within a Docker image for cross-platform compatibility.

## Installation

Installing `interpolate` requires Python [(>=v3.9)](https://wiki.python.org/moin/BeginnersGuide/Download), [pip3](https://pip.pypa.io/en/stable/installation/), and the following Python package dependencies:
  * setuptools (>=v58.0.4)
  * pytest (>=v8.4)
  * numpy (>=v2.0.2)
  * pandas (>=v2.3)
  * argparse (>=v1.4)

Once Python and `pip3` are installed on your system, `setuptools` can be installed with the following command-line command:


```
pip3 install setuptools

```

The remaining Python package dependencies and `interpolate` can be installed using the package source files provided in `interpolation-0.1.tar.gz`:

```
# Install interpolation package and dependencies
tar -zxf interpolation-0.1.tar.gz
cd interpolation-0.1/
pip3 install .

```

## Command-line usage

If your installation was successful, calling the following command should output usage documentation:

```
interpolate -h
```

The usage guide output provides details to enable you to start using the command-line tool.

```
usage: interpolate [-h] [--overwrite] [--decimals DECIMALS] input_file output_file

Replaces missing values in a table/matrix with the average of their non-diagonal neighboring
values.

positional arguments:
  input_file           Input CSV file name with tabular numeric data,`,` as the delimiter, newline
                       characters as line separators, and `nan` denoting missing values.
  output_file          Output CSV files name.

optional arguments:
  -h, --help           show this help message and exit
  --overwrite          Toggle to allow overwriting of the output file if the file name already
                       exists.
  --decimals DECIMALS  Number of decimal places to which output is rounded.
```

---

# Developer notes

The codebase for `interpolate` was designed to satisfy the requirements to produce a minimal viable product while also taking into consideration extensibility and reduction of technical debt. The `interpolate` codebase partitions the task into 3 stages:

1. Data ingestion
2. Data interpolation
3. Data export

For each of these stages I employed an object-oriented approach where I define an interface and a class to implement the interface. This provides the advantage of easier extensibility at each of the stages. The following are more concrete examples of advantages:
* Users may not always have data files in CSV format, so new classes that implement the `DataIngestor` interface can be created and easily incorporated to make data ingestion more flexible without impacting later stages. Similarly, functionality to export interpolated data in other formats than CSV may be beneficial. This also would only require separate classes for the various export formats that can be incorporated without impacting earlier stages.
* A future need may arise to use an alternative interpolation method. Incorporating a new interpolation method into the code can be done by creating a new class that implements the `Interpolator` interface. Like noted in the prior bullet point, these code changes would not impact the data ingestion and data export stages.

Although the current implementation has the advantages of modularity, one potential shortcoming is the scalability of the code when handling large matrixes that may exceed the memory resources available. In such a scenario, the code would need to be refactored to incorporate data flow (i.e., loading into RAM) in batches.

I also note below several additional enhancements to the code and software development process that I would consider implementing if more time allowed.

* The current implementation does not resolve adjacent missing values and has incomplete unit tests that I would prioritize finishing.
* Use of Python's built-in Abstract Base Classes (`abc`) module to enforce the interface contract. The current implementation is an informal interface that can provide guidance for developers but lacks enforcement of constraints.
* Addition of a Dockerfile and Docker image to provide a portable environment for the tool that promotes consistency and reproducibility. It can also promote scalability and parallelization in serverless cloud computing setups.
* Implement CI/CD concepts through GitHub actions and cloud services to:
  * Autobuild updated Docker images when Dockerfiles are updated
  * Run unit tests and code linting prior to branch merges into `main` and prior to creation of version releases.
