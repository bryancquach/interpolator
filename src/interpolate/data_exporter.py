import pandas

class DataExporter:
  """Informal interface for data exporters."""

  def export_data(self, decimals: int, overwrite: bool) -> None:
    """Write data to file.

    Args:
      decimals Number of decimal places to allow in output
      overwrite Whether to overwrite an existing file
    """
    pass


class CSVExporter(DataExporter):
  """Export data to a CSV file.

  Attributes:
    __df pandas.DataFrame for holding loaded data
    file_name Name of CSV file to where data are exported.
  """

  def __init__(self, data: pandas.DataFrame, file_name: str):
    """Constructor."""
    self.__df = data
    self.file_name = file_name

  def export_data(self, decimals=7, overwrite=False) -> None:
    """Write data to file.

    Args:
      decimals The number of decimal places to round to.
      overwrite Whether to overwrite an existing file
    """
    export_df = self.__df.round(decimals)
    if overwrite:
      write_mode = "w"
    else:
      write_mode = "x"
    export_df.to_csv(self.file_name, header=False, index=False, mode=write_mode, compression=None)
    return
