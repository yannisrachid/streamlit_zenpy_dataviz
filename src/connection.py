import zenpy
import os
import yaml
import logging

def load_params(param_file_path) -> list:
    """
    input: the name of the YAML file that contains the credentials to connect to zenpy
    ouput: two dicts (first for the credentials, second for the brands ids)
    """
    __location__ = os.getcwd()
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper
    creds = yaml.load(open(os.path.join(__location__, param_file_path)), Loader=Loader)['credentials']
    brands = yaml.load(open(os.path.join(__location__, param_file_path)), Loader=Loader)['brands']
    logging.info("Credentials loaded!")
    return creds, brands

def connect_zenpy(creds):
    """
    input: credentials (dict)
    output: zenpy client (obj)
    makes the connection to zenpy
    """
    zenpy_client = zenpy.Zenpy(**creds)
    logging.info("Successful connection to zenpy!")
    return zenpy_client

params = load_params("../params/creds.yaml")
creds = params[0]
brands = params[1]
zpc = zenpy.Zenpy(**creds)
