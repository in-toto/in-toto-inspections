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


Example usage:
python inspect_byproducts.py -l  /Users/sachitmalik/in-toto/test/demo_files/package.2dc02526.link  -st stderr -p "contains not" -s "s"
"""
import os
import sys
import argparse
import inspect
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_byproducts(link, std, presence, inputstring):

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
