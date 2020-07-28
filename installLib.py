#this is to make installing the packages a bit easier.
#I would use a requirements.txt but I don't know how to do that off the top of my head
import os
import librosa
import glob
from hashlib import sha1
import numpy as np
import pandas as pd
import scipy
from collections import Counter
import time

def install(lib):
	os.system("pip3 install " + lib)

install("librosa")
install("glob")
install("hashlib")
install("numpy")
install("pandas")
install("scipy")
install("matplotlib")
install("IPython")