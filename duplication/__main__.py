from argparse import ArgumentParser, Namespace

from duplication.detectors import NaiveDetector
from duplication.utils import write_formatted_detection_result, make_absolute_path


def main(program_args: Namespace) -> None:
    directory = make_absolute_path(program_args.directory)
    threshold = program_args.threshold
    granularity = program_args.granularity
    output = make_absolute_path(program_args.out)

    detector = NaiveDetector()
    result = detector.detect(directory, threshold, granularity)
    print(f"Writing result to {output}...")
    write_formatted_detection_result(result, output)


if __name__ == "__main__":
    parser = ArgumentParser(description="Find duplicate code in a directory")
    parser.add_argument("directory", type=str, help="directory with source code files")
    parser.add_argument("-t", "--threshold", type=float, default=0.8, help="threshold of search")
    parser.add_argument("-g", "--granularity", type=str, default="functions", help="granularity of search")
    parser.add_argument("-o", "--out", type=str, default="output.html", help="dest of result of the search")
    args = parser.parse_args()
    main(args)
