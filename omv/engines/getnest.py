import os
from ..common.inout import inform, check_output

from utils.wdir import working_dir


def install_nest():
    
    inform('Installing NEST', indent=2, verbosity=1)
    nestpath = os.path.join(os.environ['HOME'],'nest')
    nestpath2 = os.path.join(os.environ['HOME'],'nest/nest')
    os.mkdir(nestpath)
    
    with working_dir(nestpath):
        version='2.10.0'
        check_output(['wget', 'https://github.com/nest/nest-simulator/releases/download/v%s/nest-%s.tar.gz'%(version,version)])
        #check_output(['cp', '/home/padraig/temp/nest-2.4.2.tar.gz', '.'])
        check_output(['tar', 'xzvf', 'nest-%s.tar.gz'%version])
        check_output(['mv', 'nest-%s'%version, 'nest'], cwd=nestpath)
            
        check_output(["./configure", "--prefix=%s"%(nestpath2)], cwd=nestpath2)
        check_output(['make'], cwd=nestpath2)
        check_output(['make', 'install'], cwd=nestpath2)
        

if __name__ == '__main__':
    
    install_nest()










