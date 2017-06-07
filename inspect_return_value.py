"""
<Program Name>
  inspect_return_value.py
<Author>
  Sachit Malik <i.sachitmalik@gmail.com>
<Started>
  June 6, 2017
<Copyright>
  See LICENSE for licensing information.
<Purpose>

  A CLI to inspect the return value of a step.

"""
import os
import sys
import argparse
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_return_value(link, operator, integer):
    l = link_import.read_from_file(link)
    switch_dict = {'eq': (integer == l.return_value),
                   'ne': (integer != l.return_value),
                   'lt': (integer > l.return_value),
                   'le': (integer >= l.return_value),
                   'gt': (integer < l.return_value),
                   'ge': (integer <= l.return_value)}
    print(switch_dict[operator])


def main():
    """Parse the arguments and call inspect_return_value. """
    parser = argparse.ArgumentParser(
        description="Inspects the return value of a step")

    lpad = (len(parser.prog) + 1) * " "

    parser.usage = ("\n"
                    "%(prog)s --link <path to link metadata>\n{0}"
                    "[--<bash-style-boolean-operator>]\n{0}"
                    "<integer>\n{0}"
                    "[--verbose]\n\n"
                    .format(lpad))

    in_toto_args = parser.add_argument_group("in-toto-inspection options")

    in_toto_args.add_argument("-l", "--link", type=str, required=True,
                              help="Link metadata file to use for inspection of the step")

    in_toto_args.add_argument("-bsbo", "--bashstylebooleanoperator",
                              type=str, required=True, help="The boolen operator \
            used to compare the return value with given int")

    in_toto_args.add_argument("-i", "--integer", type=int, required=True,
                              help="The integer to which the return value should be compared")

    in_toto_args.add_argument("-v", "--verbose", dest="verbose",
                               help="Verbose execution.", default=False, action="store_true")

    args = parser.parse_args()

    if args.verbose:
        log.logging.getLogger.setLevel(log.logging.INFO)

    inspect_return_value(args.link, args.bashstylebooleanoperator, args.integer)


if __name__ == "__main__":
    main()
