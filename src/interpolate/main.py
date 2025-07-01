import argparse
import interpolate.data_exporter as data_exporter
import interpolate.data_ingestor as data_ingestor
import interpolate.interpolator as interpolator
import os.path

def main():
  """Main function to execute interpolation."""

  parser = argparse.ArgumentParser(
    prog="interpolate",
    description="Replaces missing values in a table/matrix with the average of their non-diagonal neighboring values.")
  parser.add_argument(dest="input_file", type=str, help="Input CSV file name with tabular numeric data,`,` as the delimiter, newline characters as line separators, and `nan` denoting missing values.")
  parser.add_argument(dest="output_file", type=str, help="Output CSV files name.")
  parser.add_argument("--overwrite", default=False, required=False, action="store_true", help="Toggle to allow overwriting of the output file if the file name already exists.")
  parser.add_argument("--decimals", type=int, default=7, required=False, help="Number of decimal places to which output is rounded.")
  args = parser.parse_args()

  # Fail-fast file and dir checks
  if not os.path.exists(args.input_file):
    raise Exception(f"{args.input_file} cannot be found.")
  if not os.path.isdir(os.path.dirname(args.output_file)):
    raise Exception(f"{os.path.dirname(args.output_file)} is not an existing directory.")
  if not args.overwrite and os.path.exists(args.output_file):
    raise Exception(f"{args.output_file} already exists and --overwrite not toggled.")

  # Ingest data
  ingestor = data_ingestor.CSVIngestor(args.input_file)
  ingestor.validate_data()
  init_data = ingestor.get_data()

  # Interpolate
  mean_interpolator = interpolator.NeighborMeanInterpolator(init_data)
  mean_interpolator.interpolate()
  interpolated_data = mean_interpolator.get_data()

  # Export interpolated data
  exporter = data_exporter.CSVExporter(interpolated_data, args.output_file)
  exporter.export_data(decimals=args.decimals, overwrite=args.overwrite)
  return

if __name__ == "__main__":
  main()
