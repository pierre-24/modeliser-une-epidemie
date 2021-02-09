set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "SIS.pdf"

set key above

set ylabel "Quantité (%)"
set xlabel "Unités de temps"

R0=1.5
set arrow from 0,1./R0*100 to 250,1./R0*100 nohead lc rgb "gray" dashtype 2
set arrow from 0,(1.-1./R0)*100 to 250,(1.-1./R0)*100 nohead lc rgb "gray" dashtype 2
set label at 5,1./R0*100-4 sprintf("S^* = %.1f\%",1./R0*100) tc rgb "gray"
set label at 5,(1-1./R0)*100-4 sprintf("I^* = %.1f\%",(1-1./R0)*100) tc rgb "gray"

plot 'SIS_R0=1.5.csv' u 1:($2*100) w l lc rgb "blue" ti "Susceptibles", '' u 1:($3*100) w l lc rgb "red" ti "Infectés"

