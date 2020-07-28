import fingerprint
import os
import librosa
import glob
from hashlib import sha1
import numpy as np
import pandas as pd
import scipy
from collections import Counter
import time

class Database:
    def __init__(self):
        self.song_table = pd.DataFrame({'song_id':[], 'name':[]})
        self.fingerprint_table = pd.DataFrame({'song_id':[], 'hash':[], 'offset':[]})
    
    def addRow(self, table, row):
        table.loc[len(table)] = row
       
    def parse_file_hash(self, filename):
        s = sha1()
        with open(filename , "rb") as f:
            while True:
                buf = f.read(2**20)
                if not buf: 
                    break
                s.update(buf)

        return s.hexdigest().upper()
        
    def add(self, f): # f is a wav file
        x, fs = librosa.load(f)
        song_id = self.parse_file_hash(f)
        self.addRow(self.song_table, [song_id, f])
        hashes = set(fingerprint.fingerprint(x, fs))
        for hash_, offset in hashes:
            self.addRow(self.fingerprint_table, [song_id, hash_, int(offset)])
        print(f'{f} is added')
            
    def get_song_by_id(self, song_id):
        return self.song_table[self.song_table['song_id'] == song_id].values[0][1]
    
    def get_song_hashes_count(self, song_id):
        return len(self.fingerprint_table.loc[self.fingerprint_table['song_id'] == song_id])
            
    def train(self, training_dir):
        t0 = time.process_time()
        i = 0
        for f in glob.iglob(training_dir+'/*.wav'):
            self.add(f)
            i += 1
        t = time.process_time()
        print(f'training time: {t-t0}; number of files added: {i}')
        
    def save(self, s, f): #s, f are both csv files. 
        self.song_table.to_csv(s)
        self.fingerprint_table.to_csv(f)
        
    def load(self, s, f):
        self.song_table = pd.read_csv(s, index_col=0)
        self.fingerprint_table = pd.read_csv(f, index_col=0)
        
    def find_matches(self, f): # f is a wav file
        x, fs = librosa.load(f)
        hashes = set(fingerprint.fingerprint(x, fs))
        return self.return_matches(hashes)
    
    def return_matches(self, hashes):
        mapper = {}
        for hash_, offset in hashes:
            mapper[hash_] = offset
        values = mapper.keys() #hashe values
        results = []
        for unique_value in set(values):
            matched = self.fingerprint_table.loc[self.fingerprint_table['hash'] == unique_value]
            if len(matched) == 0:
                continue
            else:
                for id_,offset in matched[['song_id', 'offset']].values:
                    results.append((id_, int(offset-mapper[unique_value])))
        return results
    
    def align_matches(self, matches):
        if len(matches) == 0:
            return {}
        cnt = Counter(matches)
       # for match in cnt:
           # cnt[match] /= self.get_song_hashes_count(match[0])
        best_guess = cnt.most_common(1)[0]
        largest_count = best_guess[1]
        song_id = best_guess[0][0]
        offset_difference = best_guess[0][1]
        song_name = self.get_song_by_id(song_id)
        nsec = round(float(largest_count)/44100*2048, 5)
        return {
        "SONG_ID" : song_id,
        "SONG_NAME" : song_name,
        "CONFIDENCE" : largest_count/len(matches),
        "OFFSET_DIFFERENCE" : offset_difference,
        "OFFSET_DIFFERENCE_IN_SEC": nsec
        }
    
    def query(self, f, log=True):
        t0 = time.process_time()
        output = self.align_matches(self.find_matches(f))
        t = time.process_time()
        if log:
            print("Query time:", t-t0)
        return output