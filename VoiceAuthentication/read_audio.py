import scipy.io.wavfile
from VoiceAuthentication.models import mfcc
from VoiceAuthentication.models import generate_codebook

def read_file(str):
    sample_rate, signal1 = scipy.io.wavfile.read(str)  # File assumed to be in the same directory
    #print("RERSRSFFDGDGDHHFHH",sample_rate)
#    signal1 = signal1[0:int(2 * sample_rate)]  # Keep the first 2 seconds
    signal1 = signal1[0:int(2 * sample_rate)]  # Keep the first 2 seconds
    feat1=mfcc(signal1,sample_rate,0.025,0.01,13, 26,1024,0,None,0.97,22,True)
    return feat1
#feat1=read_file('1.wav')
#print(feat1.shape)
#feat2=read_file('2.wav')
#feat3=read_file('3.wav')
#feat4=read_file('03b03Tc.wav')

#codebook1, codebook_abs_weights, codebook_rel_weights = generate_codebook(feat2, size_codebook=10, epsilon=0.00001)
