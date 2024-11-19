# Sample data injector

This script generates sample data for different datasets and injects the data into an index on a Xcyber360 indexer instance.

## Files

- `script.py`: main script file
- `connection.json`: persistence of Xcyber360 indexer connection details
- `datasets`: directory that contains the available datasets

# Getting started

1.  Install the dependencies:

```console
pip install -r requirements.txt
```

For some operating systems it will fail and suggest a different way to install it (`sudo pacman -S python-xyz`, `sudo apt install python-xyz`, etc.).

If the package is not found in this way, we can install it running `pip install -r requirements.txt --break-system-packages` (It is recommended to avoid this option if possible)

2.  Run the script selecting the dataset:

```console
python3 script.py <dataset>
```

where:

- `<dataset>`: is the name of the dataset. See the [available datasets](#datasets).

3.  Follow the instructions that it will show on the console.

# Datasets

Built-in datasets:

- decoders
- filters
- outputs
- rules

## Create dataset

1. Create a new folder on `datasets` directory. The directory name will be the name of the dataset.

2. Dataset directory:

Create a `main.py`.
This script must define a `main` function that is run when the dataset creator is called.

This receives the following parameters:

- context:
  - client: OpenSearch client to interact with the Xcyber360 indexer instance
  - logger: a logger

See some built-in dataset to know more.

# Exploring the data on Xcyber360 dashboard

The indexed data needs an index pattern that match with the index of the data to be explorable on
on Xcyber360 dashboard. So, if this is not created by another source, tt could be necessary to create
the index pattern manually if it was not previously created.

In the case it does not exist, create it with from Dashboard management > Dashboard Management > Index patterns:

- title: `xcyber360-DATASET_NAME`.

where:

- `DATASET_NAME` is the name of the dataset.

example: `xcyber360-DATASET_NAME`.

- id: `xcyber360-rules`.

where:

- `DATASET_NAME` is the name of the dataset.

example: `xcyber360-rules`.
