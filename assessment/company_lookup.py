from typing import Any


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

    def find(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """
        Find and match company data against reference sources.
        """
        pass
