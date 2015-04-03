#!/usr/bin/python

import json

makefile = open("Makefile", "w")

def w(arg):
  makefile.write(arg)

def wn(arg):
  makefile.write(arg + "\n")

def main():
  config = open("config.json")
  configData = json.load(config)

  wn("CXX\t= %s" % configData["compiler"])
  wn("CFLAGS\t= %s" % configData["cflags"])
  wn("LDFLAGS\t= %s" % configData["ldflags"])
  wn("\nSHELL\t= %s" % configData["shell"])
  wn("TEST_COUNT\t=%s" % configData["test_count"])

  wn("\n\n.PHONY: all")

  w("all: ")
  length = 0

  allSources = ""
  for source in configData["sources"]:
    length += len(source) + 1
    if length > 80:
      length = 0
      allSources += "\\\n\t"
    allSources += source.split(".")[0] + " "

  wn(allSources)
  w("\n")
  for source in configData["sources"]:
    target = source.split(".")[0]

    wn("%s: %s" % (target, source))
    wn("\t $(CXX) $(CFLAGS) -o $@ $^ $(LDFLAGS)")

  infile = configData["problem_name"] + ".in"
  okfile =  configData["problem_name"] + ".ok"
  outfile = configData["problem_name"] + ".out"

  w("\n")

  w("""TEST_SCRIPT = \\
for ((i=1; $$i <= $(TEST_COUNT); i++)); do \\
  echo "=============="; \\
  echo "Test $$i"; \\
  cp teste/$$i-%s %s; \\
  time ./$<; \\
  cp -a teste/$$i-%s %s; \\
  diff -qwB %s %s; \\
  rm %s; \\
done""" % (infile, infile, okfile, okfile, outfile, okfile, okfile))

  generator = configData["test_gen_file"]
  if configData["gen_option"] == "from_file":
    generateCode = """\\
  test=$$(head -n$$(($$i + 1)) %s tail -n1); \\
  \\
  echo "$$test" | sed 's/  */ /g' | sed 's/^ *//g' | sed 's/ *$$//g' | ./%s > infile; \\""" % \
    (configData["test_data_file"], generator)
  else:
    generateCode = """\\
  ./%s < test_config/test$$i.conf > %s;\\""" % (generator, infile)

  genExe = configData["gen_source"].rsplit('.', 1)[0]
  w("\n\n")
  wn("gen-test: " + genExe)
  w("""\t@\\
for ((i=1; $$i <= $(TEST_COUNT); i++)); do \\
  echo "Generating test $$i";""" +
  generateCode + """
  ./%s; \\
  cp %s teste/$$i-%s; \\
  cp %s teste/$$i-%s; \\
done;""" % (genExe, infile, infile, outfile, okfile))

  w("\n\n")
  for source in configData["sources"]:
    target = source.split(".")[0]
    #w("test-" + target + ": " + target + "\n")
    w("test-%s: %s\n" % (target, target))
    w("\t$(TEST_SCRIPT)\n\n")

  w("\n")
  w("clean:\n\trm -f %s" % allSources)

if __name__ == "__main__":
  main()

