from argparse import ArgumentParser
from semantic_analysis import build_parse_tree, build_program, check
from assignment2.checking import run

def parse_arguments() -> str:
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--file', required=True)
    arguments = argument_parser.parse_args()
    return arguments.file


def main():
    file_path = parse_arguments()
    parse_tree = build_parse_tree(file_path)
    program = build_program(parse_tree)
    program_meta_data = check(program)

    if program_meta_data is None:
        return
    
    variables, variables_expressions, errors = program_meta_data
    run(program, variables)


if __name__ == '__main__':
    main()