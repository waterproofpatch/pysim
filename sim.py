#!/usr/bin/env python3
import processor
import argparse

def get_program_from_file(program_file):
    """
    Get program lines from a file
    """
    return open(program_file, 'r').readlines()

def run(program_file):
    """
    Program to run
    :param program: the path to the program file
    """
    proc = processor.Processor()
    program = get_program_from_file(program_file=program_file)
    for line in program:
        line = line.strip()
        proc.perform_instruction(line)
        proc.dump_state()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Simulator")
    parser.add_argument("--program", required=True, help="path to program containing instructions to run")
    args = parser.parse_args()
    run(program_file=args.program)
