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
  operator. It prints True or False depending on the operator and
  the user supplied integer.

  Suppose the link file is located at /user/abc/def/package.45gh325.link
  and the user wants to check whether for the corresponding step(hence the link file),
  the corresponding return field contains an integer less than 5.

  The usage would be as follows:
  python inspect_return_value.py -l /user/abc/def/package.45gh325.link -bsbo "lt" -i 5

  Please note: the various bash style boolean commands are listed as follows-
  * bash-style-boolean-operator
    --eq ... equal
    --ne ... not equal
    --lt ... less than
    --le ... less than or equal
    --gt ... greater than
    --ge ... greater than or equal

  General usage:
  python inspect_return_value.py -l <path/to/the/link/file> -bsbo "<bash/style/boolean/operator>" -i <integer>


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
        A function which performs the inspection as described above depending on various arguments.
        Prints the boolean True or False depending upon the inspection result.

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
            Yet to add

        <Returns>
             None.


        """


    l = link_import.read_from_file(link)
    switch_dict = {'eq': (integer == l.return_value),
                   'ne': (integer != l.return_value),
                   'lt': (integer > l.return_value),
                   'le': (integer >= l.return_value),
                   'gt': (integer < l.return_value),
                   'ge': (integer <= l.return_value)}
    print(switch_dict[operator])




def main():

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
