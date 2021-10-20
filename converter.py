import sys
import base64


def usage():
    print("usage: -e: convert exe to output file specified /n Example:convert.py myexe.exe encoded.txt")
    sys.exit(0)

def exe_to_b64_txt(exe_file_path, output_file):
    try:
        f = open(exe_file_path, mode='rb')
        new_file = open(output_file, "w")
        raw_bin = f.read()
        encoded_bin = base64.b64encode(raw_bin)
        new_file.write(str(encoded_bin))
        return
    except Exception as exc:
        print(f"there was an error {exc.args[0]} converting {exe_file_path} to base 64 text")
        return

def line_breaker(full_string, line_length, var_name, outfile="", concat_type="+"):
    line_length = int(line_length)
    broken_string = str(var_name) + ' = '
    if concat_type == "+=":
        while (len(full_string)%line_length) > 0:
            sub_string = full_string[0:line_length]
            broken_string = broken_string + "\"" + sub_string + "\"" + '\n'
            broken_string = broken_string + var_name + ' += '
            full_string = full_string[line_length:]
        broken_string += "\"\""
    elif concat_type == "+":
        while (len(full_string)%line_length) > 0:
            sub_string = full_string[0:line_length]
            broken_string = broken_string + var_name + " + \"" + sub_string + "\"" + '\n'
            broken_string = broken_string + var_name + ' = '
            full_string = full_string[line_length:]
        broken_string += "\"\""
    if (len(outfile) > 0):
        f = open(outfile, "w")
        f.write(broken_string)
    else:
        print(broken_string)

# loads string from file
def string_loader(f):
    f = open(f, "r")
    file_contents = f.read()
    return file_contents

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    
    if (sys.argv[1] == "-e" and len(sys.argv) > 3):
        exe_to_b64_txt(sys.argv[2], sys.argv[3])

    if (sys.argv[1] == "-b" and len(sys.argv) > 4):
        if len(sys.argv) > 5:
            line_breaker(string_loader(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5])
        else:
            line_breaker(string_loader(sys.argv[2]), sys.argv[3], sys.argv[4])

    