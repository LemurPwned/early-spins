#!/bin/bash
date
/mnt/gpfs/work/plgrid/groups/plggspinsym/OOMMF/tclsh /mnt/gpfs/work/plgrid/groups/plggspinsym/OOMMF/OOMMF/oommf.tcl boxsi /mnt/gpfs/work/plgrid/groups/plggspinsym/JCH/AniaFeMgOFe/200nmMinDriver/Proba200.mif -threads 12
date
# uruchamianie: qsub -q l_long -l nodes=1:ppn=LICZBA:sl6 Skrypt.sh
#
# LICZBA to liczba uzytych watkow. Wraz z jej zwiekszaniem rosnie zarowno szybkosc symulacji jak i czas kolejkowania na gridzie. 