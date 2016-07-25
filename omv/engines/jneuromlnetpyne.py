import os
import subprocess as sp

from jneuroml import JNeuroMLEngine
from netpyne_ import NetPyNEEngine
from neuron_ import NeuronEngine

from ..common.inout import inform, trim_path, check_output, is_verbose
from engine import EngineExecutionError


class JNeuroMLNetPyNEEngine(JNeuroMLEngine):

    name = "jNeuroML_NetPyNE"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLNetPyNEEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and NetPyNEEngine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
            inform("%s installed JNeuroML..." % JNeuroMLNetPyNEEngine.name, indent=2, verbosity =1)
        if not NetPyNEEngine.is_installed(None):
            NetPyNEEngine.install(None)
            inform("%s installed NetPyNE (& NEURON)..." % JNeuroMLNetPyNEEngine.name, indent=2, verbosity =1)
            
        environment_vars_nrn, path_nrn = NeuronEngine.get_nrn_environment()

        JNeuroMLNetPyNEEngine.path = JNeuroMLEngine.path+":"+path_nrn
        JNeuroMLNetPyNEEngine.environment_vars = {}
        JNeuroMLNetPyNEEngine.environment_vars.update(JNeuroMLEngine.environment_vars)
        JNeuroMLNetPyNEEngine.environment_vars.update(NetPyNEEngine.environment_vars)
        JNeuroMLNetPyNEEngine.environment_vars.update(environment_vars_nrn)
        inform("PATH: " + JNeuroMLNetPyNEEngine.path)
        inform("Env vars: %s" % JNeuroMLNetPyNEEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLNetPyNEEngine.name), indent=1)
            self.stdout = check_output(
                ['jnml' if os.name != 'nt' else 'jnml.bat', self.modelpath, '-netpyne', '-nogui', '-run'],
                cwd=os.path.dirname(self.modelpath))
            inform("Success with running ",
                   JNeuroMLNetPyNEEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLNetPyNEEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
