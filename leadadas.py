from workflow import *

def main(file):
    w = Workflow(name="leadadas", description="""LEAD ARPS Data Analysis System (ADAS) workflow (Figure 2 in Ramakrishnan and Gannon)""")
    
    infile = File(name="input.txt", size=147*MB)
    
    tppo1 = File(name="tpp.txt", size=0.2*MB)
    tpp = Job(id="tpp", namespace="leadadas", name="TerrainPreProcessor", runtime=4*SECONDS, outputs=[tppo1])
    w.addJob(tpp)
    
    wrfstatico1 = File(name="wrfstatic.txt", size=19*MB)
    wrfstatic = Job(id="wrfstatic", namespace="leadadas", name="WrfStatic", runtime=338*SECONDS, outputs=[wrfstatico1])
    w.addJob(wrfstatic)
    
    lbio1 = File("lbi.txt", size=488*MB)
    lbi = Job(id="lbi", namespace="leadadas", name="LateralBoundaryInterpolator", runtime=146*SECONDS, inputs=[infile, tppo1], outputs=[lbio1])
    lbi.addParent(tpp)
    w.addJob(lbi)
    
    aio1 = File("ai.txt", size=243*MB)
    ai = Job(id="ai", namespace="leadadas", name="ADASInterpolator", runtime=240*SECONDS, inputs=[infile, tppo1], outputs=[aio1])
    ai.addParent(tpp)
    w.addJob(ai)
    
    wrf_dat = File("wrf.dat", size=206*MB)
    arps2wrf = Job(id="arps2wrf", namespace="leadadas", name="ARPS2WRF", runtime=78*SECONDS, inputs=[lbio1, aio1], outputs=[wrf_dat])
    arps2wrf.addParent(lbi)
    arps2wrf.addParent(ai)
    arps2wrf.addParent(wrfstatic)
    w.addJob(arps2wrf)
    
    wrf_out = File("wrf.dat.out", size=2422*MB)
    wrf = Job(id="wrf", namespace="leadadas", name="WRF", runtime=4570*SECONDS, cores=16, inputs=[wrf_dat], outputs=[wrf_out])
    wrf.addParent(arps2wrf)
    w.addJob(wrf)
    
    w.writeDAX(file)

if __name__ == '__main__':
    main("/dev/stdout")
