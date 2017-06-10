import os
import sys
import threading
import time
import traceback
import requests
import datetime
import docker
import tempfile
import json

from flask import Flask, render_template, g, request, flash, redirect, session, url_for
from queue import Queue, Empty

from constants import *

# How often the grader polls its internal queue, per second
GRADER_POLLS_PER_SEC = 2

# Seconds to wait between polling the app for new submissions
GRADER_CHECK_INTERVAL = 5

# The url for the lime app
GRADER_APP_URL = "http://localhost"

# Maximum seconds the grader is allowed to wait for a response from app
GRADER_POLLER_TIMEOUT = 5


class Grader(object):
  """ The main grader class """

  def __init__(self):
    """ Initialize the grader object """

    self.q = Queue()
    self.exit = False
    self.last_check = 0
    self.up = False

  def enqueue(self, item):
    """ Add an item to the grader queue """

    self.q.put(item)

  def _should_check(self):
    """
    Return whether the grader should check
    the app for new submissions in-queue.
    """

    return (time.time() - self.last_check >= GRADER_CHECK_INTERVAL)

  def _log(self, message):
    """ Log a message """

    print("[{:%Y-%m-%d %H:%M:%S}]: {}".format(datetime.datetime.now(), message))

  def _error(self, message, tb=True):
    """ Log an error and the latest traceback """

    self._log(message)

    if tb and sys.exc_info() != (None, None, None):
      self._log(traceback.format_exc())

  def _run(self, queue):
    """ Run the main loop of the grader object, blocking call """

    while not self.exit:
      try:
        if self._should_check():
          self._check_queue()

        message = queue.get(False)
        self._handle_message(message)
        queue.task_done()

        time.sleep(1.0 / GRADER_POLLS_PER_SEC)
      except Empty:
        # No items in queue
        pass
      except Exception as e:
        # General exception, just log it and hope it was nothing major
        self._error("Exception caught! {}".format(e))
        time.sleep(5.0)

    self._log("Grader exiting.")
    self.up = False

  def _handle_message(self, item):
    """ Handle a single item from the queue """

    self._log("Handling message!")

    if item == "check_request":
      self._check_queue()

  def _get_resource(self, path, *args, **kwargs):
    """ Fetch a resource from the app """

    if "timeout" not in kwargs:
      kwargs["timeout"] = GRADER_POLLER_TIMEOUT

    try:
      r = requests.get(GRADER_APP_URL + "/" + path, *args, **kwargs)
    except Exception as e:
      self._error("Exception while trying to fetch {}! {}".format(path, e))
      return

    # We assume every response from app is json-encoded
    try:
      data = r.json()
    except Exception as e:
      self._error("Exception while trying to parse json from path {}! {}".format(path, e))
      return

    if r.status_code == 200:
      return data

    self._log("Got a bad status code ({}) from path {}".format(r.status_code, path))
    return

  def _check_queue(self):
    """ Check the submission queue from app """

    submissions = self._get_resource("grader/queue")

    if submissions is None:
      self._log("Could not get submissions!")
      return

    if len(submissions):
      self._log("{} submissions in queue!".format(len(submissions)))

      first = submissions[0]
      self._log("Starting grading process for submission {}".format(first))

      self._grade_submission(first)

    # self._log("Checking submissions")
    self.last_check = time.time()

  def _grade_submission(self, id):
    """ Grade a submission with the given id, blocking call """

    def set_status(status, result):
      self._get_resource("grader/{}/result".format(id), params={"status": status, "result": result})

    r = self._get_resource("grader/{}/start".format(id))

    if not r:
      self._log("Failed to start the grading process for submission {}".format(id))
      return

    # download the submission data

    data = self._get_resource("grader/{}/data".format(id))

    if not data:
      set_status(STATUS_COMPLETE, RESULT_QAQ)
      return

    # create the temporary storage directory

    path = tempfile.mkdtemp()

    print("Created a temp path {}".format(path))

    # write the source

    with open("{}/source.cpp".format(path), "w") as f:
      f.write(data["code"])

    # write the grader

    with open("{}/grader.py".format(path), "w") as f:
      f.write(data["grader"])

    # create the submission.json

    submission = {
      "lang": data["lang"],
      "id": id,
      "tests": data["test_ids"],
      "file": "source.cpp",
      "time_limit": data["time_limit"],
      "memory_limit": data["memory_limit"],
    }

    with open("{}/submission.json".format(path), "w") as f:
      f.write(json.dumps(submission))

    # start the docker dockery

    logs = dclient.containers.run(
      "grader_docker",
      stdout=True,
      stderr=True,
      volumes={
        "/tests": {"bind": "/tests", "mode": "ro"},
        path: {"bind": "/subdata", "mode": "rw"}
      }
    )

    print(logs)

    try:
      with open("{}/out.json".format(path)) as f:
        result = json.loads(f.read())
    except:
      pass

    if not result or not len(result):
      set_status(STATUS_COMPLETE, RESULT_QAQ)

    print(result)

    set_status(STATUS_COMPLETE, result.get("result", RESULT_QAQ))

  def start(self):
    """ Start the main loop runner thread """

    if self.up:
      # Prevent starting two threads
      return

    self._log("Grader starting!")

    self.up = True
    self.t = threading.Thread(target=self._run, args=(self.q, ))
    self.t.start()

  def running(self):
    """ Return whether the grader has already been started """

    return self.up

dclient = docker.from_env()
g = Grader()

# Init flask

grader = Flask(__name__)
grader.secret_key = os.environ.get("FLASK_SECRET")
grader.debug = ("LIME_DEBUG" in os.environ)

# disable strict slashes in routes
grader.url_map.strict_slashes = False

# route definitions


@grader.route("/ping")
def ping():

  g.enqueue("check_request")

  if not g.running():
    g.start()

  return "pong"

if __name__ == '__main__':

  def start():
    time.sleep(0.1)

    if not g.running():
      g.start()

  t = threading.Thread(target=start)
  t.start()

  grader.run(host="127.0.0.1", port=1337, debug=True, use_reloader=False)
