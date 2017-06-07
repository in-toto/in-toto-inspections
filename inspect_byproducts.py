"""

<Program Name>
  inspect_byproducts.py

<Author>
  Sachit Malik <i.sachitmalik@gmail.com>

<Started>
  June 6, 2017

<Copyright>
  See LICENSE for licensing information.

<Purpose>

  Inspections constitute an important part of in-toto. In this script,
  we inspect the byproducts(such as stdout/stderr) of a step. The user supplies
  an input string to the program(whose presence the user wants to test),
  along with path to the corresponding link file(which link file he wants
  to test in), and a choice from stdout and stderr, and finally if the
  corresponding field of stdout/stderr is/is not/contains/contains not
  the user supplied string.

  Suppose the link file is located at /user/abc/def/package.45gh325.link
  and the user wants to check whether for the corresponding step(hence the link file),
  the corresponding stderr field contains the string "test".

  The usage would be as follows:
  python inspect_byproducts.py -l  /user/abc/def/package.45gh325.link  -st stderr -p "contains" -s "test"

  General usage:
  python inspect_byproducts.py -l  <path/to/link/metadata/file>  -st <stdout|stderr>
    -p [ "is" | "is not" | "contains" | "contains not"] -s <string to be tested>


"""


import os
import sys
import argparse
import inspect
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_byproducts(link, std, presence, inputstring):
    """

    <Purpose>
    A function which performs the inspection as described above depending on various arguments.
    Prints the boolean True or False depending upon the inspection result.

    <Arguments>
     link:
         the path to the link file

     std:
         whether to check stdout or stderr field

     presence:
         is | is not | contains | contains not

     inputstring:
         the string to be checked

     <Exceptions>
        Yet to add

    <Returns>
         None.


    """
    l = link_import.read_from_file(link)
    std_out_err = l.byproducts[std]

    if presence == 'is':
      print(std_out_err == inputstring)

    elif presence == 'is not':
      print(std_out_err != inputstring)

    elif presence == 'contains':
      if (std_out_err.find(inputstring) != -1):
            print('True')
      else:
            print('False')

    elif presence == 'contains not':
      if (std_out_err.find(inputstring) != -1):
            print('False')
      else:
            print('True')


def main():
    """Parse the arguments and call inspect_byproducts. """
    parser = argparse.ArgumentParser(
        description="Inspects the byproducts of a step")

    lpad = (len(parser.prog) + 1) * " "

    parser.usage = ("\n"
                    "%(prog)s --link <path to link metadata>\n{0}"
                    "[--stdout | --stderr]\n{0}"
                    "[--is | --is-not | --contains | --contains-not]\n{0}"
                    "<string>\n{0}"
                    "[--verbose]\n\n"
                    .format(lpad))

    in_toto_args = parser.add_argument_group("in-toto-inspection options")

    in_toto_args.add_argument("-l", "--link", type=str, required=True,
                              help="Link metadata file to use for inspection of the step")

    in_toto_args.add_argument("-st", "--outerr",
                              type=str, required=True, help="when stdout or stderr is a byproduct")

    in_toto_args.add_argument("-p", "--presence",
                              type=str, required=True, help="whether the stdout or stderr is, is not, \ "
                                                               "contains, contains not, the input string")

    in_toto_args.add_argument("-s", "--string", type=str, required=True,
                              help="The string to which the return value should be compared")

    in_toto_args.add_argument("-v", "--verbose", dest="verbose",
                               help="Verbose execution.", default=False, action="store_true")

    args = parser.parse_args()

    if args.verbose:
      in_toto.log.logging.getLogger.setLevel(log.logging.INFO)

    inspect_byproducts(args.link, args.outerr, args.presence, args.string)

if __name__ == "__main__":
    main()
