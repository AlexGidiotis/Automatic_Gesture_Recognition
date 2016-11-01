import os
import sys, subprocess
import time

#For 1 Gaussian
for i in range (1,10):
    cur_dir = "hmm"+str(i)
    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
    print cur_dir

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm0/macros', '-H', 'hmm0/hmmdefs', '-M', 'hmm1', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm1/macros', '-H', 'hmm1/hmmdefs', '-M', 'hmm2', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm2/macros', '-H', 'hmm2/hmmdefs', '-M', 'hmm3', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm3/macros', '-H', 'hmm3/hmmdefs', '-M', 'hmm4', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm4/macros', '-H', 'hmm4/hmmdefs', '-M', 'hmm5', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm5/macros', '-H', 'hmm5/hmmdefs', '-M', 'hmm6', 'hmm0/monophones0'])
herest.wait()
 
herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm6/macros', '-H', 'hmm6/hmmdefs', '-M', 'hmm7', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm7/macros', '-H', 'hmm7/hmmdefs', '-M', 'hmm8', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', 'hmm8/macros', '-H', 'hmm8/hmmdefs', '-M', 'hmm9', 'hmm0/monophones0'])
herest.wait()
    
print "HMM (1 GMM) Training Finished"

for i in range (1,10):
    cur_dir = "2gmm_hmm"+str(i)
    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
    print cur_dir
    
hhed = subprocess.Popen(['HHEd', '-H', 'hmm9/macros', '-H', 'hmm9/hmmdefs', '-M', '2gmm_hmm1', 'split.hed', 'tiedlist'])
hhed.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm1/macros', '-H', '2gmm_hmm1/hmmdefs', '-M', '2gmm_hmm2', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm2/macros', '-H', '2gmm_hmm2/hmmdefs', '-M', '2gmm_hmm3', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm3/macros', '-H', '2gmm_hmm3/hmmdefs', '-M', '2gmm_hmm4', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm4/macros', '-H', '2gmm_hmm4/hmmdefs', '-M', '2gmm_hmm5', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm5/macros', '-H', '2gmm_hmm5/hmmdefs', '-M', '2gmm_hmm6', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm6/macros', '-H', '2gmm_hmm6/hmmdefs', '-M', '2gmm_hmm7', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm7/macros', '-H', '2gmm_hmm7/hmmdefs', '-M', '2gmm_hmm8', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '2gmm_hmm8/macros', '-H', '2gmm_hmm8/hmmdefs', '-M', '2gmm_hmm9', 'hmm0/monophones0'])
herest.wait()
   
print "HMM (2 GMM) Training Finished"

#For 4 Gaussians
for i in range (1,10):
    cur_dir = "4gmm_hmm"+str(i)
    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
    print cur_dir

hhed = subprocess.Popen(['HHEd', '-H', '2gmm_hmm9/macros', '-H', '2gmm_hmm9/hmmdefs', '-M', '4gmm_hmm1', 'split.hed', 'tiedlist'])
hhed.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm1/macros', '-H', '4gmm_hmm1/hmmdefs', '-M', '4gmm_hmm2', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm2/macros', '-H', '4gmm_hmm2/hmmdefs', '-M', '4gmm_hmm3', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm3/macros', '-H', '4gmm_hmm3/hmmdefs', '-M', '4gmm_hmm4', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm4/macros', '-H', '4gmm_hmm4/hmmdefs', '-M', '4gmm_hmm5', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm5/macros', '-H', '4gmm_hmm5/hmmdefs', '-M', '4gmm_hmm6', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm6/macros', '-H', '4gmm_hmm6/hmmdefs', '-M', '4gmm_hmm7', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm7/macros', '-H', '4gmm_hmm7/hmmdefs', '-M', '4gmm_hmm8', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '4gmm_hmm8/macros', '-H', '4gmm_hmm8/hmmdefs', '-M', '4gmm_hmm9', 'hmm0/monophones0'])
herest.wait()
   
print "HMM (4 GMM) Training Finished"

#For 8 Gaussians
for i in range (1,10):
    cur_dir = "8gmm_hmm"+str(i)
    if not os.path.exists(cur_dir):
        os.makedirs(cur_dir)
    print cur_dir

hhed = subprocess.Popen(['HHEd', '-H', '4gmm_hmm9/macros', '-H', '4gmm_hmm9/hmmdefs', '-M', '8gmm_hmm1', 'split.hed', 'tiedlist'])
hhed.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm1/macros', '-H', '8gmm_hmm1/hmmdefs', '-M', '8gmm_hmm2', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm2/macros', '-H', '8gmm_hmm2/hmmdefs', '-M', '8gmm_hmm3', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm3/macros', '-H', '8gmm_hmm3/hmmdefs', '-M', '8gmm_hmm4', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm4/macros', '-H', '8gmm_hmm4/hmmdefs', '-M', '8gmm_hmm5', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm5/macros', '-H', '8gmm_hmm5/hmmdefs', '-M', '8gmm_hmm6', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm6/macros', '-H', '8gmm_hmm6/hmmdefs', '-M', '8gmm_hmm7', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm7/macros', '-H', '8gmm_hmm7/hmmdefs', '-M', '8gmm_hmm8', 'hmm0/monophones0'])
herest.wait()

herest = subprocess.Popen(['HERest','-A', '-D', '-T', '1', '-C', 'config_file', '-I', 'phones0.mlf', '-S', 'Train.scp', '-H', '8gmm_hmm8/macros', '-H', '8gmm_hmm8/hmmdefs', '-M', '8gmm_hmm9', 'hmm0/monophones0'])
herest.wait()
   
print "HMM (8 GMM) Training Finished"