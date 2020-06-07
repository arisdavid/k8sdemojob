import random
import logging
import argparse

logging.basicConfig(level=logging.INFO)


def name_shuffler(input_string):

    if isinstance(input_string, str):

        if len(input_string) < 2:
            raise Exception("Must be at least 2 characters.")

        logging.info(f"Original string: {input_string}")
        str_var = list(input_string)
        random.shuffle(str_var)

        logging.info(f"Shuffled string: {''.join(str_var)}")
    else:
        raise Exception("Input must be a string.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser("Shuffler")
    parser.add_argument("input_string", help="Input String", type=str)

    args = parser.parse_args()

    name_shuffler(args.input_string)

