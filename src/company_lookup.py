import csv
import json
import os
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Optional
from urllib.parse import urlsplit
from urllib.request import urlopen

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=1)
def _public_suffixes() -> set[str]:
    """
    Fetch the Public Suffix List once per interpreter run and cache it.
    Falls back to a small built-in set if the download fails or you are offline.
    Only the std-lib is used.
    """
    # A minimal embedded set so the function still works when offline.
    builtin = {
        "ac.uk",
        "gov.uk",
        "uk",
        "org",
        "net",
        "edu",
        "gov",
        "io",
        "ai",
        "dev",
        "biz",
        "co.uk",
        "com",
        "info",
    }

    url = "https://publicsuffix.org/list/public_suffix_list.dat"
    try:
        with urlopen(url, timeout=3) as fp:
            return {
                line.decode().strip()
                for line in fp
                if line and not line.startswith(b"//")
            }
    except Exception:
        # Network unavailable or blocked – use the built-in subset.
        return builtin


class CompanyLookup:
    """
    A class to match imperfect company data against reference
    data from Companies House and a credit bureau.

    This class provides functionality to:
    - Load and normalise reference data from Companies House and credit bureau
    - Match input company data against reference data
    - Determine match confidence based on multiple criteria
    - Return enriched company information including credit data

    Attributes:
        companies_house_data: List of company records from Companies House
        credit_bureau_data: List of credit records from credit bureau
        company_name_lookup: Dictionary mapping normalised names to company records
        credit_bureau_lookup: Dictionary mapping company numbers to credit records
    """

    def __init__(
        self, companies_house_filepath: str, credit_bureau_filepath: str
    ) -> None:
        """
        Initialize the CompanyLookup with reference data.

        Loads data from Companies House and credit bureau files, then builds
        normalised lookup dictionaries for efficient matching.

        Raises:
            FileNotFoundError: If reference data files are not found
            ValueError: If company data contains invalid names
        """

        self.companies_house_filepath = companies_house_filepath
        self.credit_bureau_filepath = credit_bureau_filepath

        self.companies_house_data: List[Dict[str, Any]] = []
        self.credit_bureau_data: List[Dict[str, Any]] = []
        self.company_name_lookup: Dict[str, Dict[str, Any]] = {}
        self.credit_bureau_lookup: Dict[str, Dict[str, Any]] = {}

        self.load_reference_data()
        self.build_normalised_company_data_lookups()
        self.build_credit_bureau_data_lookups()

    @staticmethod
    def normalise_company_name(name: Optional[str]) -> Optional[str]:
        """
        Perform normalization on company names to standardize them.

        This method:
        - Removes leading/trailing whitespace and converts to lowercase
        - Removes special characters and replaces with spaces
        - Removes common company suffixes (Group, Inc, LLC, Ltd, PLC)
        - normalises '&' to 'and'
        - Removes non-alphanumeric characters except spaces

        Args:
            name: The company name to normalise

        Returns:
            The normalised company name, or None if input is empty/None

        Examples:
            >>> CompanyLookup.normalise_company_name("ACME Corp. Ltd")
            'acme corp'
            >>> CompanyLookup.normalise_company_name("Tech & Software LLC")
            'tech and software'
        """
        if not name:
            return None

        # Remove leading and trailing whitespace and convert to lowercase
        name = name.strip().lower()

        # Remove special characters like \n, \r, and \t
        name = name.replace("\n", " ").replace("\r", " ").replace("\t", " ")

        # Replace hyphens and underscores with spaces
        name = name.replace("-", " ").replace("_", " ")

        # Replace mulitple spaces with a single space
        name = " ".join(name.split())

        # Remove common suffixes from end of string {'Group', 'Inc', 'LLC', 'Ltd', 'PLC'}
        suffixes = {"group", "inc", "llc", "ltd", "plc"}
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[: -(len(suffix) + 1)].strip()

        # Normalise "&" to "and"
        name = name.replace("&", "and")

        # Remove any remaining special characters
        name = "".join(char for char in name if char.isalnum() or char.isspace())

        # Remove any remaining leading or trailing whitespace
        name = name.strip()

        return name if name else None

    @staticmethod
    def normalise_domain(url: Optional[str]) -> Optional[str]:
        """
        normalise a URL to extract the top-level domain.

        Args:
            url: The URL to normalise

        Returns:
            The normalised domain, or None if input is empty/None

        Examples
        --------
        >>> CompanyLookup.normalise_domain("https://www.example.com:8080/path?q=1")
        'example.com'
        >>> CompanyLookup.normalise_domain("sub.domain.co.uk")
        'domain.co.uk'
        """
        if not url:
            return None

        # Strip whitespace
        url = url.strip()

        if not url:
            return None

        # Remove @ prefix if present
        if url.startswith("@"):
            url = url[1:]

        # If URL doesn't have a scheme, add one for parsing
        if not url.lower().startswith(("http://", "https://")):
            url = "http://" + url

        # Parse the URL
        parsed = urlsplit(url)
        domain = parsed.netloc

        # Remove port if present
        if ":" in domain:
            domain = domain.split(":")[0]

        # Remove www. prefix (case-insensitive)
        if domain.lower().startswith("www."):
            domain = domain[4:]

        # Convert to lowercase
        domain = domain.lower()

        return domain if domain else None

    @staticmethod
    def normalise_post_code(postcode: Optional[str]) -> Optional[str]:
        """
        normalise a postcode by removing whitespace and special characters.

        Converts to uppercase and removes all spaces, newlines, and tabs
        to create a consistent format for comparison.

        Args:
            postcode: The postcode to normalise

        Returns:
            The normalised postcode, or None if input is empty/None

        Examples:
            >>> CompanyLookup.normalise_post_code("SW1A 1AA")
            'SW1A1AA'
            >>> CompanyLookup.normalise_post_code("  m1 1aa  ")
            'M11AA'
        """
        if not postcode:
            return None

        # Remove leading and trailing whitespace and convert to uppercase
        postcode = postcode.strip().upper()

        # Remove special characters like \n, \r, and \t
        postcode = postcode.replace("\n", "").replace("\r", "").replace("\t", "")

        # Remove all spaces
        postcode = postcode.replace(" ", "")

        return postcode if postcode else None

    @staticmethod
    def normalise_date(date_str: Optional[str]) -> Optional[str]:
        """
        normalise a date string to ISO format (YYYY-MM-DD).

        Attempts to parse dates in multiple formats and converts them
        to a consistent ISO date format.

        Args:
            date_str: The date string to normalise

        Returns:
            The normalised date in ISO format, or None if input is empty/None

        Raises:
            ValueError: If the date format is not recognized

        Examples:
            >>> CompanyLookup.normalise_date("25-Jan-2025")
            '2025-01-25'
            >>> CompanyLookup.normalise_date("January 25, 2025")
            '2025-01-25'
        """
        if not date_str:
            return None

        # Try to parse the date in different formats
        try:
            # Try parsing "25-Jan-2025"
            return datetime.strptime(date_str, "%d-%b-%Y").date().isoformat()

        except ValueError:
            try:
                # Try parsing "January 25, 2025"
                return datetime.strptime(date_str, "%B %d, %Y").date().isoformat()

            except ValueError:
                try:
                    # Try parsing "2025-01-25"
                    return datetime.strptime(date_str, "%Y-%m-%d").date().isoformat()

                except ValueError:
                    raise ValueError(f"Invalid date format: {date_str}")

    def build_normalised_company_data_lookups(self) -> None:
        """
        Build lookup dictionary for normalised company names.

        Creates a dictionary mapping normalised company names to their
        corresponding company records for efficient lookup during matching.

        Raises:
            ValueError: If a company has an invalid name that cannot be normalised
        """
        self.company_name_lookup = {}

        for company in self.companies_house_data:
            normalised_name = self.normalise_company_name(company["name"])

            if not normalised_name:
                raise ValueError(f"Invalid company name: {company['name']}")

            self.company_name_lookup[normalised_name] = company

    def build_credit_bureau_data_lookups(self) -> None:
        """
        Build lookup dictionary for credit bureau data.

        Creates a dictionary mapping company numbers to their credit records,
        with normalised date formats and duplicate handling.
        """
        self.credit_bureau_lookup = {}

        for record in self.credit_bureau_data:
            company_number = str(record["company_number"])
            if company_number in self.credit_bureau_lookup:
                continue

            record["last_default_date"] = self.normalise_date(
                record["last_default_date"]
            )

            self.credit_bureau_lookup[company_number] = record

    def get_credit_bureau_record(self, company_number: str) -> Dict[str, Any]:
        """
        Retrieve credit bureau record for a given company number.

        Returns the credit record if found, otherwise returns a default
        record with None values.

        Args:
            company_number: The company number to look up

        Returns:
            Dictionary containing credit bureau information with keys:
            - company_number: The company number
            - credit_score: Credit score or None
            - trade_lines: Number of trade lines or None
            - last_default_date: Last default date or None
        """
        if self.credit_bureau_lookup.get(company_number):
            return self.credit_bureau_lookup[company_number]

        return {
            "company_number": company_number,
            "credit_score": None,
            "trade_lines": None,
            "last_default_date": None,
        }

    def load_reference_data(self) -> None:
        """
        Load reference data from Companies House and credit bureau files.

        Loads JSON data for Companies House and CSV data for credit bureau
        from the data directory.

        Raises:
            FileNotFoundError: If reference data files are not found
        """
        self.companies_house_data = self.load_json_file(self.companies_house_filepath)
        self.credit_bureau_data = self.load_csv_file(self.credit_bureau_filepath)

    def load_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load data from a JSON file.

        Args:
            file_path: Path of the JSON file to load

        Returns:
            List of dictionaries parsed from the JSON file

        Raises:
            FileNotFoundError: If the file is not found in the data directory
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found in data directory.")

        with open(file_path, "r") as file:
            return json.load(file)

    def load_csv_file(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Load data from a CSV file.

        Args:
            file_path: Path of the CSV file to load

        Returns:
            List of dictionaries parsed from the CSV file

        Raises:
            FileNotFoundError: If the file is not found in the data directory
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found in data directory.")

        with open(file_path, "r") as file:
            return [row for row in csv.DictReader(file)]

    def find(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Find and match company data against reference sources.

        Attempts to match input company data against Companies House records
        using normalised company names. Determines match confidence based on
        domain and postcode matching, and enriches results with credit data.

        Args:
            input_data: Dictionary containing company information with keys:
                - name: Company name
                - website: Company website URL
                - postcode: Company postcode
                - address: Company address

        Returns:
            Dictionary containing matched company information with keys:
            - name: Company name
            - address: Company address (dict with street, city, postcode)
            - domain: Company domain
            - company_number: Companies House number or None
            - credit_score: Credit score or None
            - last_default_date: Last default date or None
            - match_confidence: 'high', 'medium', 'low', or 'no_match'
            - trade_lines: Number of trade lines or None

        Examples:
            >>> company_lookup = CompanyLookup()
            >>> result = company_lookup.find({
            ...     "name": "ACME Corp",
            ...     "website": "https://acme.com",
            ...     "postcode": "SW1A 1AA",
            ...     "address": "123 Main St"
            ... })
            >>> result["match_confidence"]
            'high'
        """
        input_name: str = input_data["name"]
        input_website: str = input_data["website"]
        input_postcode: str = input_data["postcode"]

        normalised_input_name = self.normalise_company_name(input_name)

        if self.company_name_lookup.get(normalised_input_name):
            matched_company = self.company_name_lookup[normalised_input_name]

            normalised_input_domain = self.normalise_domain(input_website)
            normalised_input_postcode = self.normalise_post_code(input_postcode)

            normalised_company_domain = self.normalise_domain(matched_company["domain"])
            normalised_company_postcode = self.normalise_post_code(
                matched_company["address"]["postcode"]
            )

            if (
                normalised_input_domain == normalised_company_domain
                and normalised_input_postcode == normalised_company_postcode
            ):
                match_confidence = "high"

            elif (
                normalised_input_domain == normalised_company_domain
                or normalised_input_postcode == normalised_company_postcode
            ):
                match_confidence = "medium"

            else:
                match_confidence = "low"

            credit_record = self.get_credit_bureau_record(
                matched_company["company_number"]
            )

            return {
                "name": matched_company["name"],
                "address": matched_company["address"],
                "domain": matched_company["domain"],
                "company_number": matched_company["company_number"],
                "credit_score": (
                    int(credit_record["credit_score"])
                    if credit_record["credit_score"]
                    else None
                ),
                "last_default_date": credit_record["last_default_date"],
                "match_confidence": match_confidence,
                "trade_lines": (
                    int(credit_record["trade_lines"])
                    if credit_record["trade_lines"]
                    else None
                ),
            }

        else:
            return {
                "name": None,
                "address": {
                    "street": None,
                    "city": None,
                    "postcode": None,
                },
                "domain": None,
                "company_number": None,
                "credit_score": None,
                "last_default_date": None,
                "match_confidence": "no_match",
                "trade_lines": None,
            }
