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
  in-toto - installed on the path

<Purpose>
  Inspections constitute an important part of in-toto. The script take the path
  of a link file, a random string and an operator, which is used to compare
  a certain property of the link file with the random string.

  Suppose the link file is located at /user/abc/def/package.45gh325.link
  and the user wants to check whether for the corresponding step (hence the link file),
  the corresponding stderr field contains the string "test".

  The usage would be as follows:
  python inspect_byproducts.py -l  /user/abc/def/package.45gh325.link  -st stderr -o contains test

  General usage:
  python inspect_byproducts.py -l  <path/to/link/metadata/file>  -st <stdout|stderr>
    -o [ is | is not | contains | contains not] <string to be tested>


"""

import os
import sys
import argparse
import in_toto.log
from in_toto.models.link import Link as link_import
import securesystemslib.exceptions


def inspect_byproducts(link, std, operator, inputstring):
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

     inputstring:
        the string to be checked

    <Exceptions>
      Raises KeyError, in case the field corresponding to the key
        in the dictionary is empty

    <Returns>
      Integer
        0 - if the inspection is successful
        1 - if the inspection is unsuccessful
        2 - if the user supplied arguments are invalid



    """
    if not os.path.exists(link):
        print("The path to the link file is invalid")
        return 2

    else:
      l = link_import.read_from_file(link)

      try:
        std_out_err = l.byproducts[std]
      except KeyError:
        raise KeyError("The field corresponding to " + std + " in the link "
                                                             "file is empty.")

      switch_dict = {'is': (std_out_err == inputstring),
                     'is not': (std_out_err != inputstring),
                     'contains': (std_out_err.find(inputstring)),
                     'contains not': (std_out_err.find(inputstring))}

      if operator == 'is':
        if switch_dict[operator]:
          return 0

      elif operator == 'is not':
        if switch_dict[operator]:
          return 0

      elif operator == 'contains':
        if switch_dict[operator] != -1:
          return 0

      elif operator == 'contains not':
        if switch_dict[operator] == -1:
          return 0


      return 1



def main():
    """Parse the arguments and call inspect_byproducts. """
    parser = argparse.ArgumentParser(
        description="Inspects the byproducts of a step")

    lpad = (len(parser.prog) + 1) * " "

    parser.usage = ("\n"
                    "%(prog)s --link <path to link metadata>\n{0}"
                    "[--stdout | --stderr]\n{0}"
                    "[--is | --is-not | --contains | --contains-not]\n{0}"
                    "string\n{0}"
                    "[--verbose]\n\n"
                    .format(lpad))

    in_toto_args = parser.add_argument_group("in-toto-inspection options")

    in_toto_args.add_argument("-l", "--link", type=str, required=True,
                              help="Link metadata file to use for inspection "
                                  "of the step")

    in_toto_args.add_argument("-st", "--outerr",
                              type=str, required=True, help="when stdout or "
                                  "stderr is a byproduct")

    in_toto_args.add_argument("-o", "--operator",
                              type=str, required=True, help="whether the "
                                  "stdout or stderr is, is not, \ "
                                  "contains, contains not, the input string")

    in_toto_args.add_argument("string", type=str,
                              help="The string to which the return value "
                                  "should be compared")

    in_toto_args.add_argument("-v", "--verbose", dest="verbose",
                              help="Verbose execution.", default=False,
                                  action="store_true")

    args = parser.parse_args()
    args.operator = args.operator.lower()
    args.outerr = args.outerr.lower()

    if (args.operator != 'is') & (args.operator != 'is not') \
          & (args.operator != 'contains') & (args.operator != 'contains not'):
      print('Wrong operator supplied, please supply the correct operator and try again.')
      return 2

    elif (args.outerr != 'stdout') & (args.outerr != 'stderr'):
      print('Please specify only one of the following - stdout, stderr')
      return 2

    else:
      if args.verbose:
        in_toto.log.logging.getLogger.setLevel(log.logging.INFO)

      inspect_byproducts(args.link, args.outerr, args.operator, args.string)


if __name__ == "__main__":
    main()
