set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "SIRS.pdf"

set key above

set ylabel "Quantité (%)"
set xlabel "Unités de temps"

R0=2
gamma=.1
delta=.01
fac=delta/(gamma+delta)
set arrow from 0,1./R0*100 to 500,1./R0*100 nohead lc rgb "gray" dashtype 2
set label at 495,1./R0*100+4 right sprintf("S^* = %.1f\%",1./R0*100) tc rgb "gray"
set arrow from 0,fac*(1.-1./R0)*100 to 500,fac*(1.-1./R0)*100 nohead lc rgb "gray" dashtype 2
set label at 495,fac*(1-1./R0)*100+4 right sprintf("I^* = %.1f\%",fac*(1-1./R0)*100) tc rgb "gray"

plot 'SIRS_d=0.01.csv' u 1:($2*100) w l lc rgb "blue" ti "Susceptibles", '' u 1:($3*100) w l lc rgb "red" ti "Infectés", '' u 1:($4*100) w l lc rgb "green" ti "Guéris (immunisés)"

