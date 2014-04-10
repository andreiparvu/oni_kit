#!/usr/bin/python

# Makefile generator
# Copyright 2014 Bogdan Cristian Tataroiu, Andrei Parvu
# ONI 2014, Pitesti

# Consult README for further details

import json

def main():
  config = open("config.json")
  configData = json.load(config)

  makefile = open("Makefile", "w")

  makefile.write("""# Auto-generated Makefile using meta_makefile.py script.
# Do not edit unless you know what you are doing\n\n\n""")

  makefile.write("CXX\t= " + configData["compiler"] + "\n")
  makefile.write("CFLAGS\t= " + configData["cflags"] + "\n")
  makefile.write("LDFLAGS\t= " + configData["ldflags"] + "\n")
  makefile.write("\nSHELL\t= " + configData["shell"] + "\n")
  makefile.write("TEST_COUNT\t=" + configData["test_count"] + "\n")
  makefile.write("\n.PHONY: all\n")

  makefile.write("all: ")
  length = 0

  allSources = ""
  allTargets = ""
  for source in configData["sources"]:
    length += len(source) + 1
    if length > 80:
      length = 0
      allSources += "\\\n\t"
      allTargets += "\\\n\t"
    allSources += source + " "

    target = source.rsplit(".", 1)[0]
    allTargets += target + " "

  makefile.write(allTargets)
  makefile.write("\n\n")
  for source in configData["sources"]:
    target = source.rsplit(".", 1)[0]

    makefile.write(target + ": " + source + "\n")
    makefile.write("\t $(CXX) $(CFLAGS) -o $@ $^ $(LDFLAGS)\n")
    makefile.write("\n")

  infile = configData["problem_name"] + ".in"
  okfile =  configData["problem_name"] + ".ok"
  outfile = configData["problem_name"] + ".out"

  makefile.write("""TEST_SCRIPT = \\
for ((i=1; $$i <= $(TEST_COUNT); i++)); do \\
  echo "Test $$i"; \\
  cp teste/$$i-""" + infile + " " + infile + """; \\
  time ./$<; \\
  cp -a teste/$$i-""" + okfile + " " + okfile + """; \\
  diff -wBq """ + outfile + " " + okfile + """; \\
  rm """ + okfile + """; \\
done""")

  genExe = configData["gen_source"].rsplit('.', 1)[0]
  makefile.write("\n\n")
  makefile.write("gen-tests: " + genExe + "\n")
  makefile.write("""\t@\\
nr_tests=`wc -l """ + configData["test_data_file"] + """ | sed 's/  */ /g' | cut -d ' ' -f 2`; \
for ((i=2; $$i <= $$nr_tests; i++)); do \\
  test=`head -n$$(($$i + 1)) """ + configData["test_data_file"] + """ | tail -n1`; \\
  test_sanitize=`echo $$test | sed 's/  */ /g'`; \\
  nr_els=`echo $$test | wc -w | sed 's/  */ /g' | cut -d ' ' -f 2`; \\
  echo $$test_sanitize; \\
  nr_test=`echo $$test_sanitize | cut -d ' ' -f 1`; \\
  remaining_data=`echo $$test_sanitize | cut -d ' ' -f 2-$$((nr_els))`; \\
  echo $$remaining_data; \\
  echo "Generating test $$nr_test"; \\
  \\
  option=""" + configData["gen_option"] + """; \\
  if [ $$option = "simple" ]; then \\
    echo $$remaining_data > """ + infile + """; \\
  elif [ $$option = "single_file" ]; then \\
    echo $$remaining_data | ./""" + configData["test_gen_file"] + " > " + infile + """; \\
    ./""" + genExe + """; \\
  elif [ $$option = "multiple_files" ]; then \\
    cat $$remaining_data | ./""" + configData["test_gen_file"] + " > " + infile + """; \\
    ./""" + genExe + """; \\
  fi; \\
  cp """ + infile + " teste/$$nr_test-" + infile + """; \\
  cp """ + outfile + " teste/$$nr_test-" + okfile + """; \\
done; \\
\\
make clean;""")

  makefile.write("\n\n")
  for source in configData["sources"]:
    target = source.split(".")[0]
    makefile.write("test-" + target + ": " + target + "\n")
    makefile.write("\t$(TEST_SCRIPT)\n\n")

  makefile.write("\n")
  makefile.write("clean:\n\trm -f " + allTargets + "\n")

if __name__ == "__main__":
  main()

