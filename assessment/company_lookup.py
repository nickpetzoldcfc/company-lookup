from typing import Any
import typing
import json
import csv
import re
from urllib.parse import urlparse
from pydantic import BaseModel


def read_json_as_dict(filepath: str) -> typing.List[dict]:
    data = []
    with open(filepath, 'r') as fp:
        data = json.load(fp)
    return data


class CompaniesHouseRecord(BaseModel):
    company_number: str = None
    name: str = None
    domain: str = None
    address: dict = None

    @property
    def clean_name(self):
        name = self.name.lower().strip()
        name_with_org_identifiers = re.sub(r"(inc|ltd|group|llc|PLC)", "", name)
        clean_name = re.sub(r"[^a-z0-9 ]", "", name_with_org_identifiers)
        return "".join(clean_name.split())

    @property
    def clean_postcode(self):
        postcode = self.address['postcode'].lower().strip()
        return "".join(postcode.split())

    @property
    def is_valid_domain(self):
        parsed_url = urlparse(self.domain.lower())
        scheme = parsed_url.scheme
        if scheme and scheme not in ['http', 'https']:
            return False
        return True

    @property
    def clean_domain(self):
        domain = self.domain.lower()
        domain = re.sub(r"www.", "", domain)
        parsed_url = urlparse(domain)
        netloc = parsed_url.netloc
        if netloc:
            return netloc
        website_path = parsed_url.path
        if website_path:
            return website_path.split("/")[0]


class ResponseModel(BaseModel):
    name: typing.Optional[str] = None
    domain: typing.Optional[str] = None
    address: dict  = {'city': None, 'postcode': None, 'street': None}
    company_number: typing.Optional[str] = None
    credit_score: typing.Optional[str] = None
    last_default_date: typing.Optional[str] = None
    trade_lines: typing.Optional[str] = None
    match_confidence: str = "no_match"


def read_csv_as_dict(filepath: str) -> typing.List[dict]:
    data = []
    with open(filepath, 'r') as csvfile:
        csv_dict = csv.DictReader(csvfile)
        for row in csv_dict:
            data.append(row)
    return data


def prepare_companies_house_data(filepath: str) -> typing.List[CompaniesHouseRecord]:
    comapnies_house_data = read_json_as_dict(filepath)
    return [CompaniesHouseRecord(**row) for row in comapnies_house_data]

def prepare_credit_bureau_data(filepath: str) -> dict[str, Any]:
    credit_bureau_data = read_csv_as_dict(filepath)
    credit_bureau_dict = dict()
    for row in credit_bureau_data:
        credit_bureau_dict[row['company_number']] = row
    return credit_bureau_dict


class CompanyLookup:
    """
    A class to match imperfect company data against reference
    data from Companies House and a credit bureau.
    """

    def __init__(
        self, companies_house_filepath: str, credit_bureau_filepath: str
    ) -> None:
        """
        Initialize the CompanyLookup with reference data.
        """

        self.companies_house_filepath = companies_house_filepath
        self.credit_bureau_filepath = credit_bureau_filepath
        self.companies_house_data_list = prepare_companies_house_data(self.companies_house_filepath)
        self.credit_bureau_data_dict = prepare_credit_bureau_data(self.credit_bureau_filepath)

    @staticmethod
    def _modify_input_data(data: dict[str, Any]) -> dict[str, Any]:
        return {
            "address": {'postcode': data['postcode']},
            "domain": data['website'],
            "name": data["name"],
        }

    @staticmethod
    def compare_data_and_derive_confidence(input_data: dict[str, Any], match_data: CompaniesHouseRecord):

        input_data = CompanyLookup._modify_input_data(input_data)
        input_data = CompaniesHouseRecord(**input_data)

        if input_data.clean_name == match_data.clean_name and input_data.clean_postcode == match_data.clean_postcode and input_data.is_valid_domain and input_data.clean_domain == match_data.clean_domain:
            return "high"
        elif input_data.clean_name == match_data.clean_name and input_data.clean_postcode == match_data.clean_postcode:
            return "medium"
        elif input_data.clean_name == match_data.clean_name:
            return "low"
        return "no_match"


    def find(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Find and match company data against reference sources.
        """

        """
        sample companies house

        """
        # Implementation of the matching logic goes here

        for record in self.companies_house_data_list:
            comfidence = self.compare_data_and_derive_confidence(input_data, record)
            if comfidence not in ['no_match']:
                response_dict = record.dict()
                credit_data = self.credit_bureau_data_dict.get(record.company_number)
                if credit_data:
                    response_dict.update(credit_data)
                return ResponseModel(match_confidence=comfidence, **response_dict).dict()

        return ResponseModel().dict()






