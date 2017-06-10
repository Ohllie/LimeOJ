import os
import sys
import subprocess
import json
import psutil
import time
import threading
import tempfile

TESTS_PATH = "/tests"
TEMP_PATH = "/subdata"

RESULT_ND = 0
RESULT_AC = 1
RESULT_WA = 2
RESULT_TLE = 3
RESULT_MLE = 4
RESULT_CE = 5
RESULT_QAQ = 6

class CompileException(Exception): pass

def temp_file(name):
  return "{}/{}".format(TEMP_PATH, name)

def load_submission_data():
  """ Load the metadata of the submission """

  try:
    with open(temp_file("submission.json")) as f:
      return json.loads(f.read())
  except Exception as e:
    pass

def compile_code(file):
  """ Compile the given cpp code with g++ """

  with open(temp_file(file)) as f:
    print(f.read())

  p = subprocess.Popen(["g++", temp_file(file), "-O2", "-o", "program", "-Wall", "-Wextra", "--std=c++11"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout, stderr = p.communicate()

  if p.returncode != 0:
    raise CompileException(stderr)

def run_test(id, memory_limit=64, time_limit=1, extra_time=0.05):
  """ Run a single test case """

  # check that the input exists
  if not os.path.exists("/tests/{}".format(id)):
    raise Exception("Test missing")

  # read the data
  inp = ""
  with open("/tests/{}/input".format(id)) as f:
    inp = f.read()

  # start the program and feed stdin
  p = subprocess.Popen(["./program"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  pp = psutil.Process(pid=p.pid)

  class Result(object):
    def __init__(self):
      self.res = None
    def set(self, r):
      self.res = r

  def monitor(res):
    start = time.time()

    while True:
      should_exit = True
      
      try:
        exists = psutil.pid_exists(p.pid)
        should_exit = not exists
      except:
        pass

      if should_exit:
        break

      try:
        mem_info = pp.memory_info()
      except:
        break

      if mem_info.rss > memory_limit * 1024 * 1024:
        p.send_signal(9)
        res.set(RESULT_MLE)

      if time.time() - start > time_limit + extra_time:
        p.send_signal(9)
        res.set(RESULT_TLE)

      time.sleep(0.01)

    return

  r = Result()
  monitor = threading.Thread(target=monitor, args=(r,))
  monitor.start()

  stdout, _ = p.communicate(input=inp.encode("ascii"))

  # wait for the monitor to exit
  monitor.join()

  if r.res:
    return {
      "result": r.res
    }

  # write the stdout to a temp file
  
  fname = None
  with tempfile.NamedTemporaryFile(delete=False) as f:
    f.write(stdout)
    fname = f.name

  # run the grader on this program
  p = subprocess.Popen(["python3", temp_file("grader.py"), fname, "{}/{}/output".format(TESTS_PATH, id)])
  stdout, stderr = p.communicate()

  if p.returncode == 0:
    return {
      "result": RESULT_AC
    }

  return {
    "result": RESULT_WA
  }

def grade():
  """ Grade the submission """

  SUB_DATA = load_submission_data()

  if not SUB_DATA:
    return {
      "result": RESULT_QAQ,
      "message": "System Error"
    }

  try:
    compile_code(SUB_DATA["file"])
  except Exception as e:
    return {
      "result": RESULT_CE,
      "message": str(e)
    }

  time_limit =  SUB_DATA.get("time_limit", 1)
  memory_limit =  SUB_DATA.get("memory_limit", 64)

  test_ids = SUB_DATA["tests"]
  test_results = {}

  for test in test_ids:
    result = run_test(test, time_limit=time_limit, memory_limit=memory_limit)

    test_results[test] = result

  if all(x["result"] == RESULT_AC for x in test_results.values()):
    overall = RESULT_AC
  elif any(x["result"] == RESULT_MLE for x in test_results.values()):
    overall = RESULT_MLE
  elif any(x["result"] == RESULT_TLE for x in test_results.values()):
    overall = RESULT_TLE
  else:
    overall = RESULT_WA

  return {
    "result": overall
  }    

if __name__ == '__main__':
  grade_out = grade()

  with open("{}/out.json".format(TEMP_PATH), "w") as f:
    f.write(json.dumps(grade_out))
