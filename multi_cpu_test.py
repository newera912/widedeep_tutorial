import numpy as np
import tensorflow as tf
import datetime


#Processing Units logs
log_device_placement = True

#num of multiplications to perform
n = 5


# Example: compute A^n + B^n on 2 CPUs

# Create random large matrix
#A = np.random.rand(1e4, 1e4).astype('float32')
#B = np.random.rand(1e4, 1e4).astype('float32')
A = np.random.rand(3e3, 3e3).astype('float32')
B = np.random.rand(3e3, 3e3).astype('float32')

# Creates a graph to store results
c1 = []
c2 = []

# Define matrix power
def matpow(M, n):
    if n < 1: #Abstract cases where n < 1
        return M
    else:
        return tf.matmul(M, matpow(M, n-1))

with tf.device('/cpu:0'):
    a = tf.constant(A)
    b = tf.constant(B)
    #compute A^n and B^n and store results in c1
    c1.append(matpow(a, n))
    c1.append(matpow(b, n))

with tf.device('/cpu:0'):
  sum = tf.add_n(c1) #Addition of all elements in c1, i.e. A^n + B^n

t1_1 = datetime.datetime.now()
with tf.Session(config=tf.ConfigProto(log_device_placement=log_device_placement)) as sess:
    # Runs the op.
    sess.run(sum)
t2_1 = datetime.datetime.now()


print t2_1 - t1_1




# Multi CPU computing
# CPU:0 computes A^n
with tf.device('/cpu:0'):
    #compute A^n and store result in c2
    a = tf.constant(A)
    c2.append(matpow(a, n))

#CPU:1 computes B^n
with tf.device('/cpu:1'):
    #compute B^n and store result in c2
    b = tf.constant(B)
    c2.append(matpow(b, n))

with tf.device('/cpu:2'):
  sum = tf.add_n(c2) #Addition of all elements in c2, i.e. A^n + B^n

t1_2 = datetime.datetime.now()
with tf.Session(config=tf.ConfigProto(device_count={'CPU': 3},log_device_placement=log_device_placement)) as sess:
    # Runs the op.
    sess.run(sum)
t2_2 = datetime.datetime.now()

print t2_2 - t1_2
