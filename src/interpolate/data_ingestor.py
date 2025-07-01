import os.path
import pandas
import warnings

class DataIngestor:
  """Informal interface for data ingestors.

  Attributes:
    validated Boolean indicating loaded data is validated and conforms to expectations.
  """

  validated: bool

  def _load_data(self) -> pandas.DataFrame:
    """Read data from file."""
    pass

  def validate_data(self) -> None:
    """Check that data conforms to expectations."""
    pass

  def get_data(self) -> pandas.DataFrame:
    """Retrieve loaded data."""
    pass


class CSVIngestor(DataIngestor):
  """Data ingestor for data in a CSV file.

  Attributes:
    validated Boolean indicating loaded data is validated and conforms to expectations
    file_name Name of CSV file containing data to load
    __df pandas.DataFrame for holding loaded data
  """

  validated = False

  def __init__(self, file_name: str):
    """Constructor."""
    assert os.path.exists(file_name), f"{file_name} not found"
    self.file_name = file_name
    self.__df = self._load_data()

  def _load_data(self) -> pandas.DataFrame:
    """Read data from CSV file.

    Returns:
      pandas.DataFrame: Data loaded from file
    """
    csv_data = pandas.read_csv(self.file_name, header=None)
    self.validated = False
    return csv_data

  def validate_data(self) -> None:
    """Check that data conforms to expectations.

    Returns:
      None
    """
    if not (self.__df.dtypes == float).all():
      raise RuntimeError("Ingested data contains values that are not type `float`")
    if sum(self.__df.shape) == 0:
      raise RuntimeError("Data ingestion resulted in empty DataFrame. Is your CSV file empty?")
    if self.__df.shape[0] == 1:
      warnings.warn("Data ingestion resulted in a single row. Verify this is expected and that your newline character is correct", UserWarning)
    if self.__df.shape[1] == 1:
      warnings.warn("Data ingestion resulted in a single column. Verify this is expected and that you are using a comma delimiter", UserWarning)
    self.validated = True
    return
  
  def get_data(self) -> pandas.DataFrame:
    """Retrieve loaded data.

    Returns:
      pandas.DataFrame: Data loaded from file
    """
    if not self.validated:
      warnings.warn("Data has not been validated", UserWarning)
    return self.__df
