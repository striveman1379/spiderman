
import os
import shutil
import argparse
import socket

start_path = os.path.join(os.path.dirname(__file__), 'start.py')
log_path = os.path.join(os.getcwd(), '.logs')

def start(args):
    # create logs
    if os.path.isdir(log_path): shutil.rmtree(log_path)
    os.mkdir(log_path)

    for i in range(args.processes):
        log_file_path = os.path.join(log_path, 'spider_{0}.log'.format(i))
        params = '-s SPIDER_ID={0}@{1}'.format(socket.gethostname(), i)
        cmd = 'nohup python {0} crawl imdb {1} > {2} &'.format(start_path, params, log_file_path)
        print(cmd)
        os.system(cmd)



def stop(args):
    search_cmd = "ps -ef | grep start.py | awk '{print $2}'"
    pids = os.popen(search_cmd).read().split('\n')
    kill_cmd = 'kill -9 '
    for pid in pids:
        kill_cmd += pid
        kill_cmd += ' '

    print(os.popen(kill_cmd).read())



if __name__ == '__main__':
    def str2bool(v): return v.lower() in ("yes", "true", "t", "1", True)
    parser = argparse.ArgumentParser(description="Run commands")
    parser.add_argument('command', choices=["start", "stop"], help="choice command")
    parser.add_argument('--processes', default=1, type=int, help='processes count')
    args = parser.parse_args()

    if args.command == 'start':
        start(args)

    elif args.command == 'stop':
        stop(args)