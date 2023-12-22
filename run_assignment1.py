from argparse import ArgumentParser
from semantic_analysis import check, build_program, build_parse_tree
from assignment1.lock_tree.checking import run

def parse_arguments() -> tuple[str, str]:
    argument_parser = ArgumentParser()
    argument_parser.add_argument('--file-1', required=True)
    argument_parser.add_argument('--file-2', required=True)
    arguments = argument_parser.parse_args()
    return arguments.file_1, arguments.file_2


def main():
    file_path_1, file_path_2 = parse_arguments()
    programs = []
    for parse_tree in [build_parse_tree(file_path) for file_path in [file_path_1, file_path_2]]:
        program = build_program(parse_tree)
        program_meta_data = check(program)

        if program_meta_data is None:
            return
        
        variables, variables_expressions, errors = program_meta_data

        if variables_expressions is None:
            return
        
        programs.append((program, variables_expressions, errors))
    
    run(tuple(programs))


if __name__ == '__main__':
    main()
