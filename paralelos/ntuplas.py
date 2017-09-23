import os
dst_file = []
for i in xrange(1,34):
        i = str(i)
        if int(i)<10:
                dst_file_name = '/scratch13/MC2012MB/00040748_0000000'+i+'_2.AllStreams.dst'
        else:
                dst_file_name = '/scratch13/MC2012MB/00040748_000000'+i+'_2.AllStreams.dst'

        if os.path.isfile(dst_file_name):
                dst_file.append(dst_file_name)
