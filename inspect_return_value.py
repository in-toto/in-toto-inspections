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
  Inspections constitute an important part of in-toto. In this script,
  we inspect the return value of a step. The user supplies an integer
  to the program(as compared to which the user wants to test various
  boolean operators), along with path to the corresponding link file
  (which link file he wants to test in), and also a bash style boolean
  operator.

  Suppose the link file is located at /user/abc/def/package.45gh325.link
  and the user wants to check whether for the corresponding step (hence the
  link file), the corresponding return field contains an integer less than 5.

  The usage would be as follows:
  python inspect_return_value.py -l /user/abc/def/package.45gh325.link -o lt 5

  Please note: the various bash style boolean commands are listed as follows-
  * bash-style-boolean-operator
    --eq ... equal
    --ne ... not equal
    --lt ... less than
    --le ... less than or equal
    --gt ... greater than
    --ge ... greater than or equal

  General usage:
  python inspect_return_value.py -l <path/to/the/link/file> -o <operator>
    <integer>

"""
import os
import sys
import argparse
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_return_value(link, operator, integer):
    """
    <Purpose>
      A function which performs the inspection as described above depending
      on various arguments.

    <Arguments>
      link:
        the path to the link file

      operator:
        bash style boolean operator

      integer:
        the integer to which the return value should be compared
        Note: the comparison happens treating the integer as a consequent,
        for example: given "lt" as an operator, it will inspect whether
        (the return value) <= (the given integer)

    <Exceptions>
      None

    <Returns>
      Boolean

    """

    imported_link = link_import.read_from_file(link)
    if operator == 'eq':
      return integer == imported_link.return_value

    elif operator == 'ne':
      return integer != imported_link.return_value

    elif operator == 'lt':
      return integer > imported_link.return_value

    elif operator == 'le':
      return integer >= imported_link.return_value

    elif operator == 'gt':
      return integer < imported_link.return_value

    elif operator == 'ge':
      return integer <= imported_link.return_value

    else:
      raise('Invalid operator ' + operator + '. Valid operators: eq | ne | '
        'lt | le | gt | ge')

    return False

def parse_args():

    """
    <Purpose>
      A function which parses the user supplied arguments.

    <Arguments>
      None

    <Exceptions>
      None

    <Returns>
      Parsed arguments (args object)

    """
    parser = argparse.ArgumentParser(
        description="Inspects the return value of a step")

    lpad = (len(parser.prog) + 1) * " "

    parser.usage = ("\n"
                    "%(prog)s --link <path to link metadata>\n{0}"
                    "[--operator ('eq' | 'ne' | 'lt' | 'le' | 'gt' | "
                      "'ge')]\n{0}"
                    "<integer>\n\n"
                    .format(lpad))

    in_toto_args = parser.add_argument_group("in-toto-inspection options")

    in_toto_args.add_argument("-l", "--link", type=str, required=True,
                              help="Link metadata file to use for inspection "
                              "of the step")

    in_toto_args.add_argument("-o", "--operator", choices=['eq', 'ne',
                              'lt', 'le', 'gt', 'ge'], type=str,
                              required=True, help="The logical operator "
                              "used to compare the return value with given "
                              "int")

    in_toto_args.add_argument("integer", type=int,
                              help="The integer to which the return value "
                              "should be compared")

    args = parser.parse_args()
    args.operator = args.operator.lower()

    return args


def main():
    """
    First calls parse_args() to parse the arguments and then calls
    inspect_return_value to inspect the return value.

    """
    args = parse_args()

    try:
      if inspect_return_value(args.link, args.operator, args.integer):
        sys.exit(0)
      else:
        sys.exit(1)
    except Exception as e:
      print('The following error occured', e)
      sys.exit(2)


if __name__ == "__main__":
    main()
