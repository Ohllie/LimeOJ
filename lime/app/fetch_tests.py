import requests
import os

APP_URL = "http://localhost"

TESTS_PATH = "/tests"


def get_json(path, debug=False):
  try:
    url = "{}/{}".format(APP_URL, path)

    if debug:
      print("Getting url {}".format(url))

    r = requests.get(url, timeout=1)

    if r.status_code != 200:
      raise Exception("Bad status code, {}".format(r.status_code))

    return r.json()
  except Exception as e:
    raise e


def fetch_tests():
  test_ids = get_json("grader/testids")
  for test in test_ids:

    print("Getting test #{}".format(test))

    test_data = get_json("grader/{}/testdata".format(test))

    path = "{}/{}".format(TESTS_PATH, test)

    if not os.path.exists(path):
      os.makedirs(path)

      print("Created {}".format(path))

    # write the test data in files

    with open("{}/input".format(path), 'w') as f:
      f.write(test_data["input"])

    with open("{}/output".format(path), 'w') as f:
      f.write(test_data["output"])

if __name__ == '__main__':
  fetch_tests()
