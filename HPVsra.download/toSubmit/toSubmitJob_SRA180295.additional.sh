qsub -cwd -q ionode.q -pe OpenMP 1 -m ae -M yanj@gis.a-star.edu.sg -l mem_free=10G,h_rt=24:0:0 /mnt/projects/yanj/hcc/HPVsra.download/job.SRA180295/downLoad_SRR1609136.sh
qsub -cwd -q ionode.q -pe OpenMP 1 -m ae -M yanj@gis.a-star.edu.sg -l mem_free=10G,h_rt=24:0:0 /mnt/projects/yanj/hcc/HPVsra.download/job.SRA180295/downLoad_SRR1609148.sh

