"""
<Program Name>
  inspect_byproducts.py

<Author>
  Sachit Malik <i.sachitmalik@gmail.com>

<Started>
  June 6, 2017

<Copyright>
  See LICENSE for licensing information.

<Requires>
  in-toto

<Purpose>
  Inspections constitute an important part of in-toto. The script take the path
  of a link file, a random string and an operator, which is used to compare
  a certain property of the link file with the random string.

  Suppose the link file is located at /user/abc/def/package.45fe325.link
  and the user wants to check whether for the corresponding step (hence the
  link file), the corresponding stderr field contains the string "test".

  The usage would be as follows:
  python inspect_byproducts.py -l  /user/abc/def/package.45fe325.link  -t
    stderr -o contains test

  General usage:
  python inspect_byproducts.py -l  <path/to/link/metadata/file>  -t
    <stdout|stderr> -o [ is | is not | contains | contains not] <string to
    be tested>
"""

import os
import sys
import argparse
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_byproducts(link, type, operator, input_string):
    """
    <Purpose>
    A function which performs the inspection as described above depending on
    various arguments.

    <Arguments>
      link:
        the path to the link file

      std:
        whether to check stdout or stderr field

      operator:
        is | is not | contains | contains not

      input_string:
        the string to be checked

    <Exceptions>
      Raises KeyError, in case the field corresponding to the key
      in the dictionary is empty

    <Returns>
      Boolean
    """

    imported_link = link_import.read_from_file(link)

    std_out_err = imported_link.byproducts[type]

    if operator == 'is':
      if std_out_err == input_string:
        return True

    elif operator == 'is-not':
      if std_out_err != input_string:
        return True

    elif operator == 'contains':
      if std_out_err.find(input_string) != -1:
        return True

    elif operator == 'contains-not':
      if std_out_err.find(input_string) == -1:
        return True
    else:
        raise Exception(
            "Invalid operator {}. Valid operators: is | is-not | contains | "
            "contains-not".format(operator))

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
        description="Inspects the byproducts of a step")

    in_toto_args = parser.add_argument_group("in-toto-inspection options")

    in_toto_args.add_argument("-l", "--link", type=str, required=True,
                              help="Path to the link file to be inspected",
                              metavar="<Path to link metadata>")

    in_toto_args.add_argument("-t", "--type", choices=['stdout', 'stderr'],
                              type=str, required=True, help="Type of "
                              "byproduct to inspect (stdout | stderr")

    in_toto_args.add_argument("-o", "--operator", choices=['is', 'is-not',
                              'contains', 'contains-not'], type=str,
                              required=True, help="whether "
                              "stdout or stderr is, is not,"
                              "contains, contains not, the input string")

    in_toto_args.add_argument("string", type=str,
                              help="The string to compare with the specified "
                              "byproduct in the specified link file",
                              metavar="<String to compare>")

    args = parser.parse_args()
    args.operator = args.operator.lower()
    args.type = args.type.lower()

    return args


def main():
    """
    First calls parse_args() to parse the arguments and then calls
    inspect_byproducts to inspect the byproducts
    """
    args = parse_args()
    try:
      if inspect_byproducts(args.link, args.type, args.operator, args.string):
        sys.exit(0)
      else:
        sys.exit(1)
    except Exception as e:
      print('The following error occured', e)
      sys.exit(2)


if __name__ == "__main__":
    main()
