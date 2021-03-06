from utils import config
import os
import subprocess


conf = config.conf()


def main():
    '''   
    pcap:   .PCAP file in FS. Will replace file extension with CSV to FS path.
    #add option to capture interface i='eth0' sampling local traffic / tcpdump samples'
    '''

    pcap_path = os.path.join(conf['fspath'], conf['processfile'] + '.pcap')
    csv_path = os.path.join(conf['fspath'], conf['processfile'] + '.csv')
    

    # Add UDP ports, or really all proto ports in one column (two src/dst)
    tshk=' '.join([
          'sudo tshark',
          #'-i eth0',
          '-r {}'.format(pcap_path),
          #'-a duration:{}'.format(duration),
          #'-c 20', #testing
          '-T fields',
          '-e frame.number',
          '-e frame.time',
          '-e frame.len',
          #'-e eth.src',
          #'-e eth.dst',
          '-e ip.proto',
          '-e _ws.col.Protocol',
          '-e ip.src',
          '-e ip.dst',
          '-e tcp.srcport',
          '-e tcp.dstport',
          '-e udp.srcport',
          '-e udp.dstport',
          '-e tcp.seq',
          '-e tcp.flags',
          #'-e tcp.payload',
          #'-e frame.protocols',
          '-E header=y',
          '-E separator=,',
          '-E quote=d',
          '-E occurrence=f',
          '> {}'.format(csv_path),
          ])

    print('Running tshark on {}...'.format(pcap_path))
    sp=subprocess.Popen(tshk, shell=True, stdin=None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = sp.communicate()
    print(csv_path)

if __name__=='__main__':
    main()

