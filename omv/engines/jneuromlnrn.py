import os
import subprocess as sp

from omv.engines.jneuroml import JNeuroMLEngine
from omv.engines.neuron_ import NeuronEngine
from omv.common.inout import inform, trim_path, check_output, is_verbose
from omv.engines.engine import EngineExecutionError


class JNeuroMLNRNEngine(JNeuroMLEngine):

    name = "jNeuroML_NEURON"

    @staticmethod
    def is_installed(version):
        if is_verbose():
            inform("Checking whether %s is installed..." %
               JNeuroMLNRNEngine.name, indent=1)
        return JNeuroMLEngine.is_installed(None) and NeuronEngine.is_installed(None)

    @staticmethod
    def install(version):

        if not JNeuroMLEngine.is_installed(None):
            JNeuroMLEngine.install(None)
        if not NeuronEngine.is_installed(None):
            NeuronEngine.install(None)
            
        environment_vars_nrn, path_nrn = NeuronEngine.get_nrn_environment()

        JNeuroMLNRNEngine.path = JNeuroMLEngine.path + \
            ":" + path_nrn
        JNeuroMLNRNEngine.environment_vars = {}
        JNeuroMLNRNEngine.environment_vars.update(
            JNeuroMLEngine.environment_vars)
        JNeuroMLNRNEngine.environment_vars.update(
            environment_vars_nrn)
        inform("PATH: " + JNeuroMLNRNEngine.path)
        inform("Env vars: %s" % JNeuroMLNRNEngine.environment_vars)

    def run(self):
        try:
            inform("Running file %s with %s" % (trim_path(self.modelpath), JNeuroMLNRNEngine.name), indent=1)
            self.stdout = check_output(
                ['jnml' if os.name != 'nt' else 'jnml.bat', self.modelpath, '-neuron', '-nogui', '-run'],
                cwd=os.path.dirname(self.modelpath))
            inform("Success with running ",
                   JNeuroMLNRNEngine.name, indent=1)
            self.returncode = 0
        except sp.CalledProcessError as err:
            inform("Error with ", JNeuroMLNRNEngine.name, indent=1)
            self.returncode = err.returncode
            self.stdout = err.output
            raise EngineExecutionError
