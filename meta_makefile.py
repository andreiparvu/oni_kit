#!/usr/bin/python

import json

def main():
  config = open("config.json")
  configData = json.load(config)

  makefile = open("Makefile", "w")

  makefile.write("CXX\t= " + configData["compiler"] + "\n")
  makefile.write("CFLAGS\t= " + configData["cflags"] + "\n")
  makefile.write("LDFLAGS\t= " + configData["ldflags"] + "\n")
  makefile.write("\nSHELL\t= " + configData["shell"])
  makefile.write("TEST_COUNT\t=" + configData["test_count"])
  makefile.write("\n\n.PHONY: all\n")

  makefile.write("all: ")
  length = 0

  allSources = ""
  for source in configData["sources"]:
    length += len(source) + 1
    if length > 80:
      length = 0
      allSources += "\\\n\t"
    allSources += source + " "

  makefile.write(allSources)
  makefile.write("\n")
  for source in configData["sources"]:
    target = source.split(".")[0]

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
  diff -wB """ + outfile + " " + okfile + """; \\
  rm""" + okfile + """; \\
done""")

  genExe = configData["gen_source"].rsplit('.', 1)[0]
  makefile.write("\n\n")
  makefile.write("gen-test: " + genExe + "\n")
  makefile.write("""\t@\\
for ((i=1; $$i <= $(TEST_COUNT); i++)); do \\
  echo "Generating test $$i"; \\
  test=$$(head -n$$(($$i + 1)) """ + configData["test_data_file"] + """ tail -n1); \\
  \\
  echo "$$test" | sed 's/  */ /g' | sed 's/^ *//g' | sed 's/ *$$//g' | ./""" + configData["test_gen_file"] + " > " + infile + """; \\
  ./""" + genExe + """; \\
  cp """ + infile + "teste/$$i-" + infile + """; \\
  cp """ + outfile + "teste/$$i-" + okfile + """; \\
done; \
\
make clean;""")

  makefile.write("\n\n")
  for source in configData["sources"]:
    target = source.split(".")[0]
    makefile.write("test-" + target + ": " + target + "\n")
    makefile.write("\t$(TEST_SCRIPT)\n\n")

  makefile.write("\n")
  makefile.write("clean: " + allSources + "\n")

if __name__ == "__main__":
  main()

