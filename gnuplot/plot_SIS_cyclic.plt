set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "SIS_cyclic.pdf"

set key above

set ylabel "Quantité (%)"
set xlabel "Unités de temps"

set xrange [0:1000]

plot 'SIS_cyclic.csv' u 1:($3*100) w l lc rgb "red" lw 2 ti "Infectés", '' u 1:($4*100) w l lc rgb "black" ti "{/Symbol b}(t)"

