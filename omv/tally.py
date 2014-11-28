from collections import OrderedDict
from common.inout import trim_path


class Tallyman(object):
    def __init__(self, mepomt):
        self.omt = mepomt.omt_path
        self.mep = mepomt.mep_path
        self.backend = mepomt.engine
        self.modelpath = mepomt.modelpath
        self.experiments = {}

    def all_passed(self):
        alltrue = True if any(self.experiments) else False
        for res in self.experiments.values():
            alltrue = alltrue and all(res.values())
        return alltrue
        
    def add_experiment(self, exp, results):
        self.experiments[exp.name] = results

    def serialize(self):
        s = OrderedDict({'backend': self.backend})
        s['MEP file'] = self.mep
        s['OMT file'] = self.omt
        s['Model path'] = self.modelpath
        s['Experiments'] = self.experiments
        s['All Passed'] = self.all_passed()
        #return dump(s, default_flow_style=False)
        return s
    
    def __repr__(self):
        return str(self.serialize())


class TallyHolder(object):
    
    tallies = {}
    all_engines = []
    
    def add(self, tally):
        
        if not tally.backend in self.all_engines:
            self.all_engines.append(tally.backend)
            
        mp = trim_path(tally.modelpath)
        
        if not self.tallies.has_key(mp):
            self.tallies[mp] = {}
        
        mptallies = self.tallies[mp]
        
        if not mptallies.has_key(tally.backend):
            mptallies[tally.backend] = []
            
        mptallies[tally.backend].append(tally)
        
    def summary(self):
        width1 = 60
        border = '+'+'-'*width1+'+'
        header = '|'+' '*width1+'| '
        
        totals = {}
        for engine in self.all_engines:
            border += '-'*(len(engine)+2)+"+"
            header += engine+' | '
            totals[engine]=0
        
        summary = '%s\n%s\n%s\n' %(border, header, border)
        
        
        for mp in self.tallies.keys():
            
            mp_ = mp
            max = width1 -2
            if len(mp_)>max:
                pre = 8
                mp_ = '%s(...)%s'%(mp_[:pre],mp_[-1*(max - pre - 6):])
                
            summary += '| '+mp_+' '*(width1-len(mp_)-2)+" |   "
            
            mptallies = self.tallies[mp]
            
            for engine in self.all_engines:
                if not mptallies.has_key(engine):
                    
                    info = "%s"%(' ')
                    summary += ' '*(len(engine)-len(info)-2)+info+" |   "
                else:
                    tals = mptallies[engine]
                    for t in tals:
                        if t.backend == engine:
                            info = "%s"%(len(t.experiments))
                            totals[engine]+=len(t.experiments)
                            summary += ' '*(len(engine)-len(info)-2)+info+" |   "
            summary += '\n'
            
        summary += border+'\n'+'| Totals: '+' '*(width1-9)+'|   '
        
        for engine in self.all_engines:
            info = "%s"%(totals[engine])
            summary += ' '*(len(engine)-len(info)-2)+info+" |   "
                
        summary += '\n'+border
        return summary
        
        
        