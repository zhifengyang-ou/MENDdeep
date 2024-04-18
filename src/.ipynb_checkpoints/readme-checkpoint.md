## added one big leaf canopy GPP model (FBEM.F90) to MEND through MEND_IN.F90

1. the inputs and control variables (.nml) are in folder photosyn

2. Plotting figures with python script and need to fix by removing the space in df[' An']

2. run with long-term climate, lai data from Biocon

    a. copied from Genie Folder
    
    b. fix auto-compile and link (see runScript.txt)
    
    c. **due to no soil water data, I treat it as 0.35 and comment out read(13...), all the above code are ineffective** (water is used for ecosystem respiration)
    
    d. uploaded it to github under ecosys_mend; will create another branch (nfeedback) for nitrogen feedback to photosynthesis
    
            1) borrow functions from soil water limitation on gpp from teco (not so good)
            2) try exp(ax)/(1+exp(ax))