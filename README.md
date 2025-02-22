<div align="center">
  <h1>W&M PEP FEA</h1>
  <h5>Finite Element Analysis for the W&M PEP Competition Craft</h5>
</div>

> [!CAUTION]
> If you are reading this, and you are not affiliated with William & Mary, or its PEP team, especially if you are part of another team, I already have your IP, home address, and eye color. I _will_ find you.

## Installation/Usage

Before installing this repository, ensure that you have [OpenFOAM](https://www.openfoam.com/) installed on a machine you have access to.

Clone the repository:

```bash
git clone git@github.com:jc-campbell/pep-fea.git
```

Create a virtual environment (recommended) and install dependencies:

```bash
pip install
```

This repository is currently set up to run the simulations on a remote linux-based server over SSH. Local and Windows support is... claimed to be in development.

Once everything is installed, you should be able to use the `pipeline.ipynb` notebook to run anything in the `/cases` directory, or to build your own cases.
