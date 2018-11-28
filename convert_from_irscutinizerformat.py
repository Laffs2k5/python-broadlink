"""Helper script for convert irScrutinizer export to Openhab map format"""
import argparse
import binascii

# Helper
def add_zeros_for_broadlink_format(in_str):
    # Multiples of 32 required by openhab broadlink add-on
    # Add zeroes according to modulus of 32
    mod_of_32 = (len(in_str) + 8) % 32
    if mod_of_32 != 0:
        missing_zeros_count = 32 - mod_of_32
        #print 'was: ' + in_str  # debug
        in_str += ('0' * missing_zeros_count)
        #print ' is: ' + in_str  # debug
    return in_str

# Support
def print_command(commandDefPrefix,commandDefName,commandDefPayload):
    # type: (str, str, str) -> None
    toReplace = {
        '+': 'plus',
        '-': 'minus',
        ' ': '_',
        '/': '_',
        ':': '_'
        }
    for key, value in toReplace.iteritems():
        commandDefName = commandDefName.replace(key, value)
    print commandDefPrefix.upper() + commandDefName.upper() + "=" + str(commandDefPayload)

# "Main"
def convert_from(irScutinizerFile,specific_ir_command=None,specific_ir_command_repetitons=None):
    """Start convert ir codes to openhab map format"""

    # import stuff
    name = 'commands'
    commands = getattr(__import__(irScutinizerFile, fromlist=[name]), name)

    name = 'get_command_data'
    get_command_data = getattr(__import__(irScutinizerFile, fromlist=[name]), name)

    # print the stuff
    if specific_ir_command is not None:
        ir_payload = get_command_data(specific_ir_command, specific_ir_command_repetitons)
        ir_payload_broadlink = add_zeros_for_broadlink_format(binascii.hexlify(ir_payload))
        if (specific_ir_command_repetitons > 1):
            #print irScutinizerFile.upper() + specific_ir_command.upper() + "_X" + str(specific_ir_command_repetitons) + "=" + ir_payload_broadlink
            print_command(irScutinizerFile,specific_ir_command + "_X" + str(specific_ir_command_repetitons),ir_payload_broadlink)
        else:
            #print irScutinizerFile.upper() + specific_ir_command.upper() + "=" + ir_payload_broadlink
            print_command(irScutinizerFile,specific_ir_command,ir_payload_broadlink)
    else:
        for ir_command, ir_data in commands.iteritems():
            ir_payload = get_command_data(ir_command, 1)
            ir_payload_broadlink = add_zeros_for_broadlink_format(binascii.hexlify(ir_payload))
            #print irScutinizerFile.upper() + ir_command.replace() .upper() + "=" + ir_payload_broadlink
            print_command(irScutinizerFile,ir_command,ir_payload_broadlink)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("--file", help="irScrutinizer-file to cinvert")
    parser.add_argument("--command", help="Output payload for specific command only")
    parser.add_argument("--count", default=1, type=int, help="Repetitions of ir connabd")
    args = parser.parse_args()

    if args.file:
        # Sanitize
        if args.file.startswith('.\\'):
            args.file = args.file[2:]
        if args.file.endswith('.py'):
            args.file = args.file[:-3]
        elif args.file.endswith('.pyc'):
            args.file = args.file[:-4]

        # Convert
        if args.command:
            convert_from(args.file, args.command, args.count)
        else:
            convert_from(args.file)

