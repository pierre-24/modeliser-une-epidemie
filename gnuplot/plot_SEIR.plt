set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "SEIR.pdf"

set key above

set ylabel "Quantité (%)"
set xlabel "Unités de temps"

plot 'SEIR_R0=2.csv' u 1:($3*100) w l lc rgb "orange" ti "Exposés", '' u 1:($4*100) w l lc rgb "red" ti "Infectés", 'SIR_R0=2.csv' u 1:($3*100) w l lc rgb "red" dashtype 2 notitle

