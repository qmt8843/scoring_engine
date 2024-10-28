import subprocess

website_process = subprocess.Popen(['python', "website.py"])
scoring_process = subprocess.Popen(['python', "scoring.py"])

website_process.wait()
scoring_process.wait()