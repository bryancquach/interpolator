import pandas
import pytest
import src.interpolate.data_ingestor as data_ingestor

@pytest.fixture
def ingestor_object():
  """Create a CSVIngestor object to use with tests."""
  input_file = "data/examples/input_test_data.csv"
  return data_ingestor.CSVIngestor(input_file)

def test_csv_ingestor_construction(ingestor_object):
  assert ingestor_object.validated == False
  assert type(ingestor_object.file_name) == str
  assert type(ingestor_object.get_data()) == pandas.DataFrame #will throw a UserWarning

#TODO: Test CSVIngestor.validate_data()

#TODO: Test CSVIngestor.get_data()
