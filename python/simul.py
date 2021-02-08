from dynamic.parser import Parser
import argparse
import math

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    
    parser.add_argument('file', type=argparse.FileType('r'), help='file that describe the system')
    parser.add_argument('-t', '--time', help='Time before stop', type=int, default=200)
    parser.add_argument('-d', '--dt', help='timestep for simulation', type=float, default=.1)
    parser.add_argument('-D', '--dt-print', help='timestep for printing', type=float, default=1.)
    
    args = parser.parse_args()
    
    # parse
    cs = Parser(args.file.read()).parse()
    
    # compute
    print('t\t' + '\t'.join(c.name for c in cs.compartiments))
    print(cs)
    
    dt = args.dt
    tprint = int(args.dt_print / dt)
    n = 0
    while abs(args.time - cs.t) >= dt:
        cs.step(dt)
        n += 1
        if n % tprint == 0:
            print(cs)

if __name__ == '__main__':
    main()
        
