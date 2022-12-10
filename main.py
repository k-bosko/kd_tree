from argparse import ArgumentParser, FileType
from time import perf_counter

from algos.colors import get_colors
from algos.naive import NaiveConverter
from algos.scipy_kdtree import ScipyKDTreeConverter
from algos.custom_kdtree import CustomKDTreeConverter

if __name__ == '__main__':
    parser = ArgumentParser(
        prog='KD_Tree',
        description='Measuring the performance of KD Trees for solving the nearest neighbor problem.',
    )

    parser.add_argument(
        '--input',
        '-i',
        dest='input',
        type=str,
    )
    parser.add_argument(
        '--output',
        '-o',
        dest='output',
        type=str,
    )
    parser.add_argument(
        '--colors',
        '-c',
        dest='colors',
        type=FileType('r'),
    )
    parser.add_argument(
        '--naive',
        '-n',
        dest='is_naive',
        action='store_true',
    )
    parser.add_argument(
        '--scipy',
        '-s',
        dest='is_scipy',
        action='store_true',
    )
    parser.add_argument(
        '--kdtree',
        '-k',
        dest='is_custom',
        action='store_true',
    )
    args = parser.parse_args()
    colors = get_colors(args.colors)

    start = perf_counter()
    if args.is_naive:
        print('Naive Conversion')
        conversion = NaiveConverter(args.input, colors)
    elif args.is_scipy:
        print('Scipy KD Tree Conversion')
        conversion = ScipyKDTreeConverter(args.input, colors)
    elif args.is_custom:
        print('Custom KD Tree Conversion')
        conversion = CustomKDTreeConverter(args.input, colors)
    else:
        print('Please specify either -k, -s or -n to choose an algorithm')
        exit(1)

    conversion.convert()
    print(f'Timing: {perf_counter() - start}')

    conversion.save_file(args.output)
