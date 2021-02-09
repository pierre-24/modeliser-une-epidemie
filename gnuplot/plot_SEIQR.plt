set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "SEIQR.pdf"

set key above

set ylabel "Quantité (%)"
set xlabel "Unités de temps"

plot 'SEIR_R0=2.csv' u 1:($4*100) w l lc rgb "red"  dashtype 2 notitle,\
 'SEIQR_G=0.01.csv' u 1:($4*100) w l lc rgb "red" ti "Infectés",\
 '' u 1:($5*100) w l lc rgb "dark-green" title "Quarantaine"

