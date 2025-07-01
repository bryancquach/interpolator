import numpy as np
import pandas

class Interpolator:
  """Informal interface for data interpolators."""

  def interpolate(self) -> None:
    """Perform interpolation for all NaN values."""
    pass

  def get_data(self) -> pandas.DataFrame:
    """Retrieve data.."""
    pass


class NeighborMeanInterpolator(Interpolator):
  """Interpolator using neighboring values in DataFrame.

  Interpolator that averages neighboring values to estimate a replacement value for a NaN.

  Attributes:
    nan_indices A list of DataFrame indices corresponding to NaN values
    __df pandas.DataFrame for holding data for interpolation
  """

  def __init__(self, data: pandas.DataFrame):
    """Constructor."""
    self.__df = data
    self.nan_indices = list(zip(*np.where(self.__df.isna())))

  def __get_mean(self, neighbor_indices) -> float:
    """Calculate mean of DataFrame values based on an index list.

    NaN values pointed to from indices are excluded from the mean calculation.

    Args:
      neighbor_indices A list of row,column index pairs for values to use in calculations

    Returns:
      float The calculated mean
    """
    neighbors = [self.__df.iloc[x[0], x[1]] for x in neighbor_indices]
    mean_val = np.nanmean(neighbors) 
    return mean_val

  def interpolate(self, use_diag=False) -> None:
    """Perform interpolation for all NaN values.

    Performs interpolation by averaging neighbor values. If all neighbor values are NaN then
    an error will be thrown.

    Args:
      use_diag boolean for whether diagonal neighbors should be included

    Returns:
      None
    """
    for i in range(len(self.nan_indices)):
      row, col = self.nan_indices[i]
      init_neighbor_indices = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
      if use_diag:
        init_neighbor_indices += [(row + 1, col + 1), (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1)]
      # Remove index pairs that are not valid
      filtered_neighbor_indices = []
      for index_pair in init_neighbor_indices:
        i,j = index_pair
        if i < 0 or i >= self.__df.shape[0] or j < 0 or j >= self.__df.shape[1]:
          # Index out of range
          continue
        else:
          filtered_neighbor_indices.append(index_pair)
      # Replace with interpolated value
      new_val = self.__get_mean(filtered_neighbor_indices)
      if np.isnan(new_val):
        raise Exception(f"Error: Value could not be interpolated for index ({row}, {col})")
      self.__df.iat[row, col] = new_val
    return

  def get_data(self) -> pandas.DataFrame:
    """Retrieve data.

    Returns:
      pandas.DataFrame Interpolation data
    """
    return self.__df
