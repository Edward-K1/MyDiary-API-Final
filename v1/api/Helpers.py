""" This module contains functions that validate data according to
 the specified fields and their regex validation patterns """

import re


def validate_and_assemble_data(data, fields, regx_patterns, help_messages):
    """
    Returns a tuple with 3 values:

    1 -> Validity: Boolean indicating whether the data is valid according
    to the passed values

    2 -> assembled_data: a list of data arranged according to the fields passed

    3 -> message: a message indicating missing, invalid, or excess fields if any.

    It expects dictionary for data, a list for fields, a list for regx patterns
    that are to be used during validation and list of help messages to show for
    each invalid field found

    """
    missing_fields = []
    excess_fields = []
    invalid_fields = []
    assembled_data = []
    message = ''
    Validity = False

    missing_fields.extend([x for x in fields if x not in data])
    excess_fields.extend([k for k in data.keys() if k not in fields])

    if missing_fields:
        message = f"The following fields were missing in the data: {','.join(missing_fields)}"

        return (Validity, assembled_data, message)

    if excess_fields:
        message = f"The following excess fields were ignored: {','.join(excess_fields)}"

    for count, field in enumerate(fields):

        m = re.match(regx_patterns[count], str(data.get(field)))

        if not m:
            invalid_fields.append(field)


        dt = data.get(field)

        if str(dt).strip() != "":
            assembled_data.append(dt)
        else:
            invalid_fields.append(field)

    if invalid_fields:
        message = prepare_invalid_fields_help(fields,invalid_fields,help_messages)
        return (Validity, assembled_data, message)

    Validity = True

    return (Validity, assembled_data, message)



def prepare_invalid_fields_help(fields,invalid_fields,fields_help):
    """This function formats the invalid fields and returns them with their help"""
    invalids_list={}

    msg=f"The following fields had invalid data: {','.join(invalid_fields)}"

    invalids_list["error"]=msg

    help_messages=""

    for count,field in enumerate(fields):
        if field in invalid_fields:
            help_messages+=field + " -> "+fields_help[count] + " "

    invalids_list["help"]=help_messages


    return invalids_list


def assign_data(cls, data: list):
    """
        This method returns class instances with their respective arguments
        when <= 10

        """
    # This unnecessary repetition was supposed to be handled by a single tuple e.g cls(tuple(data))
    # which is valid in python 3 but for some reason, it was rejected when passed to the classes.

    length = len(data)

    if length == 1:
        return cls(data[0])
    elif length == 2:
        return cls(data[0], data[1])
    elif length == 3:
        return cls(data[0], data[1], data[2])
    elif length == 4:
        return cls(data[0], data[1], data[2], data[3])
    elif length == 5:
        return cls(data[0], data[1], data[2], data[3], data[4])
    elif length == 6:
        return cls(data[0], data[1], data[2], data[3], data[4], data[5])
    elif length == 7:
        return cls(data[0], data[1], data[2], data[3], data[4], data[5],
                   data[6])
    elif length == 8:
        return cls(data[0], data[1], data[2], data[3], data[4], data[5],
                   data[6], data[7])
    elif length == 9:
        return cls(data[0], data[1], data[2], data[3], data[4], data[5],
                   data[6], data[7], data[8])
    elif length == 10:
        return cls(data[0], data[1], data[2], data[3], data[4], data[5],
                   data[6], data[7], data[8], data[9])
