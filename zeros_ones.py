tf = open('zeros_one.txt', 'w')
number = 576
for i in range(0,number):
    tf.write(' 0.0')
tf.write('\n')
for i in range(0,number):
    tf.write(' 1.0')
tf.close()