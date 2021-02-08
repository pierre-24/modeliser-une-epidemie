set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "Re.pdf"
set multiplot

set key above

set xrange [1:7.5]
set yrange [0:60]

set ylabel "Quantité (%)"
set xlabel "R_{e}"

set label at 1.92,50 "◼ S* = 50%" tc rgb "blue" font ",12"
set label at 1.92,2.5 "◼ I* = 2,5%" tc rgb "red" font ",12"
set arrow from 2, graph 0 to 2, graph 1 nohead lc rgb "gray" dashtype 2

alpha=.005
beta=.2
plot (1./x)*100 w l ls 1 lc rgb "blue" ti 'S*',\
  (alpha/beta*(x-1))*100  w l lc rgb "red" ti 'I*'
