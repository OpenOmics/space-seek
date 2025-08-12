#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Python standard library
from __future__ import print_function
import csv, sys

# Local imports
from utils import (
    Colors,
    err,
    fatal
)

# Constants
_C = Colors()
# Required sample sheet field names
REQUIRED_SAMPLE_SHEET_COLUMNS = [
    "sample",
    "fastqs",
    "cytaimage",
    "slide",
    "area"
]
# Optional sample sheet field names,
# with their default values, most
# of which are None. The id field
# is set to the required sample field
# if it is provided.
OPTIONAL_SAMPLE_SHEET_COLUMNS = [
    "id",
    "image",
    "darkimage",
    "colorizedimage",
    "loupe_alignment",
    "barcode_csv"
]

# Helper functions
def stripped(s):
    """Cleans string to remove quotes from its leading
    and trailing ends.
    @param s <str>:
        String to remove quotes or clean
    @return s <str>:
        Cleaned string with quotes removed
    """
    return s.strip('"').strip("'").strip()


def index_file(input_file, key, required_fields, optional_fields, delim=','):
    """Parses and indexes a file into a dictionary for quick
    lookups later. The file will be indexed as a nested dictionary
    where key is the first key and the second keys are the required
    and optional fields. 
    For example, if the file, sample_sheet.csv, contains the following:
    sample,fastqs,cytaimage,slide,area,image,id
    A,/path/to/fastq1,cytaimage1,slide1,area1,,
    B,/path/to/fastq2,cytaimage2,slide2,area2,image2,IDB
    >>> index_file("sample_sheet.tsv", "sample",
        ["fastqs","cytaimage","slide","area"],
        ["image", "id"])
    {
        "A": {
            "fastqs": "/path/to/fastq1",
            "cytaimage": "cytaimage1",
            "slide": "slide1",
            "area": "area1",
            "image": "",
            "id": ""
        },
        "B": {
            "fastqs": "/path/to/fastq2",
            "cytaimage": "cytaimage2",
            "slide": "slide2",
            "area": "area2",
            "image": "image2",
            "id": "IDB"
        }
    }
    @param input_file <str>:
        File to parse and index. Must contain a header with
        the columns listed in required_fields. The index of
        these columns will be automatically resolved.  
    @param key <str>:
        Column name of the first key to index the file by.
    @param required_fields <list[str]>:
        List of required column names that will be used as
        the second key to index the file. The values of these
        columns will be stored in a nested dictionary.
    @param optional_fields <list[str]>:
        List of optional column names that will be used as
        the second key to index the file. The values of these
        columns will be stored in a nested dictionary. If a
        column is not present in the file, it will be set to
        the value provided in the dictionary.
    @param delim <str>:
        Delimiter used to separate columns in the file.
        Default is a comma (',').
    @return file_idx <dict[key][required_fields|optional_fields]=str>:
        Nested dictionary where,
            • key = 'key' column value
            • value = {required_field_col: "A", optional_field_col: "B"}
        Given,
            key="A", required_fields=["C","D"]
            returns {"A": {"C": "c_i", "D": "d_i"}}
    """
    errors = False   # Used to track errors
    file_idx = {}    # Nested dictionary with parsed file
    line_number = 0  # Used for error reporting 
    with open(input_file, newline='') as fh:
        # Skip empty lines and comments
        file = csv.DictReader(
            (line for line in fh if line.strip() and not line.lstrip().startswith("#")),
            delimiter=delim
        )
        for parsed_line in file:
            line_number += 1
            # Add first key to file_idx
            _k1 = stripped(parsed_line[key])
            if _k1 not in file_idx:
                file_idx[_k1] = {}
            # Check for required fields
            for field in required_fields:
                value = stripped(parsed_line.get(field, ''))
                if field not in parsed_line or not value:
                    # Missing required field from header
                    err(
                        "Error: Missing required field '{}' in line {} of file '{}'!".format(
                            field, line_number, input_file
                        )
                    )
                    errors = True
                    continue # goto next field
                # Add required field to file_idx
                file_idx[_k1][field] = stripped(parsed_line[field])
            # Check for optional fields
            for field in optional_fields:
                value = stripped(parsed_line.get(field, ''))
                if field not in parsed_line or not value:
                    # Missing optional field from header,
                    # or empty value
                    value = ''
                # Add optional field to file_idx
                file_idx[_k1][field] = value
    # Check for errors
    if errors:
        fatal(
            "Fatal: Errors were found while parsing file '{}'! Please fix the errors and try again.".format(input_file)
        )
    return file_idx


def sample_sheet(
        file,
        required_fields=REQUIRED_SAMPLE_SHEET_COLUMNS,
        optional_fields=OPTIONAL_SAMPLE_SHEET_COLUMNS,
        remap_missing_fields={"id": "sample"}
    ):
    """Parses a sample sheet file and returns an indexed dictionary.
    The sample sheet must contain a header with the required fields.
    @param file <str>:
        Path to the sample sheet file to parse and index. This can be a
        .tsv, .txt, or .csv file. The file must contain a header with
        the required fields.
    @param required_fields <list[str]>:
        List of required field names that must be present in the header.
    @param optional_fields <list[str]>:
        List of optional field names that can be present in the header.
    @param remap_missing_fields <dict[str]=str>:
        Dictionary to remap missing fields to required fields.
        For example, if the sample sheet does not contain an 'id' field,
        it can be remapped to the 'sample' field which will always be
        present.
    """
    if file.endswith('.tsv') or file.endswith('.txt'):
        # Use tab as delimiter for TSV files
        delim = '\t'
    elif file.endswith('.csv'):
        # Use comma as delimiter for CSV files
        delim = ','
    else:
        # Unsupported file type, not sure what the
        # delimiter is here or what the user is trying
        # to do, so we will raise an error.
        fatal(
            "Error: Unsupported file type for sample sheet '{}'. "
            "Fatal: Please provide a .tsv (tab-seperated) or .csv (comma-seperated) file.".format(file)
        )
    # Parse and index the sample sheet
    parsed_file = index_file(
        file,
        "sample",
        required_fields,
        optional_fields,
        delim=delim
    )
    # Remap missing fields to a required field
    for sample, metadata in parsed_file.items():
        for field, remap_field in remap_missing_fields.items():
            if field not in metadata or not metadata[field]:
                # If the field is missing or empty, remap it
                # to a known required field. We are using this
                # to remap the 'id' field to the 'sample' field
                # if the 'id' field was not provided or it is
                # set to an empty string/value.
                metadata[field] = metadata.get(remap_field, '')
    return parsed_file


if __name__ == "__main__":
    # Testing sample sheet parser
    input_sample_sheet = sys.argv[1] # supports .tsv, .txt, .csv
    parsed_file = sample_sheet(
        input_sample_sheet
    )
    # Print nest dictionary with
    # parsed sample sheet values
    print(parsed_file)
