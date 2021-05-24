from argparse import ArgumentParser, Namespace

from potator.detectors import NaiveDetector, FilteringDetector
from potator.utils import write_formatted_detection_result, make_absolute_path
from potator.profiler import Profile


def parse_args() -> Namespace:
    parser = ArgumentParser(description="Find duplicate code in a directory")
    parser.add_argument("directory", type=str, help="directory with source code files")
    parser.add_argument("-d", "--detector", type=str, choices=["Naive", "Filtering"], help="type of detector to use")
    parser.add_argument("--depth", type=int, default=1, help="depth of adaptive prefix for FilteringDetector")
    parser.add_argument("-t", "--threshold", type=float, default=0.8, help="threshold of search")
    parser.add_argument("-g", "--granularity", type=str, default="functions", help="granularity of search")
    parser.add_argument("-o", "--out", type=str, default="output.html", help="dest of result of the search")
    args = parser.parse_args()
    return args


def main() -> None:
    program_args = parse_args()
    directory = make_absolute_path(program_args.directory)
    threshold = program_args.threshold
    granularity = program_args.granularity
    output = make_absolute_path(program_args.out)
    detector_type = program_args.detector
    depth = program_args.depth

    detector = NaiveDetector()
    if detector_type == "Filtering":
        detector = FilteringDetector(depth)

    with Profile("detection"):
        result = detector.detect(directory, threshold, granularity)

    print(f"Writing result to {output}...")
    write_formatted_detection_result(result, output)


if __name__ == "__main__":
    main()
