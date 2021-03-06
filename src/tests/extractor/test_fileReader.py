import unittest
import os
from datetime import datetime

from extractor.fileReader import FileReader
from extractor.entities.saleRawData import SaleRawData

DATA_FOLDER = "../data"
TEST_FILE = "example pp 15 rows.csv"
TEST_FILE_HEADERS = "example pp 15 rows with header.csv"
TEST_FILE_ONE_LINE = "example pp 1 row.csv"

class fileReaderTest(unittest.TestCase):

    def test_read_when_file_has_headers(self):
        file_ = self._getTestFilePath(TEST_FILE_HEADERS)

        # execute
        reader = FileReader()
        reader.read(file_, True) # has headers

        assert not reader.errors
        data = reader.records
        assert data is not None
        self.assertEqual(15, len(data), "size of result (records number)")

        assert isinstance(data[0], SaleRawData)


    def test_read_when_file_has_not_headers(self):

        file_ = self._getTestFilePath(TEST_FILE)

        # execute
        reader = FileReader()
        reader.read(file_)

        assert not reader.errors
        data = reader.records
        assert data is not None
        self.assertEqual(15, len(data), "size of result (records number)")


    def test_read__should__return_the_expected_RawPriceData_object(self):

        file_ = self._getTestFilePath(TEST_FILE_ONE_LINE)

        # execute
        reader = FileReader()
        reader.read(file_)

        data = reader.records

        expected_date = datetime(2002, 5, 31)

        record: SaleRawData = data[0]
        self.assertEqual("{4E95D757-1CA7-EDA1-E050-A8C0630539E2}", record.transaction_id, "transaction_id")
        self.assertEqual(970000, record.price, "price")
        self.assertEqual(expected_date, record.date, "date")
        self.assertEqual("SW3 2BZ", record.post_code, "post_code")
        self.assertEqual("F", record.property_type, "property_type")
        self.assertEqual("N", record.new_build, "new_build")
        self.assertEqual("L", record.holding_type, "holding_type")

        self.assertEqual("paon", record.paon, "paon")
        self.assertEqual("saon", record.saon, "saon")
        self.assertEqual("street", record.street, "street")
        self.assertEqual("locality", record.locality, "locality")
        self.assertEqual("city", record.city, "city")
        self.assertEqual("district", record.district, "district")
        self.assertEqual("county", record.county, "county")

        self.assertEqual("transaction_category", record.transaction_category, "transaction_category")
        self.assertEqual("action", record.action, "action")


    def _getTestFilePath(self, file_name):

        # os.getcwd() can be wrong (depends on the settings of the test configuration)
        current_dir = os.path.dirname(os.path.realpath(__file__))
        test_file = os.path.join(current_dir, DATA_FOLDER, file_name)
        return test_file