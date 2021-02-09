set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "R0.pdf"
set multiplot

set key above

set xrange [1:7.5]
set yrange [0:100]

set ylabel "Quantité (%)"
set xlabel "R_{0}"
set y2label "Temps (unités arbitraires)"
set ytics nomirror
set y2tics
set y2range [0:100]

set arrow from 2, graph 0 to 2, graph 1 nohead lc rgb "gray" dashtype 2
set label at 1.92,15.85 "◼ I_{max} = 15,8%" tc rgb "red" font ",12"
set label at 1.92,43.8 "◼ t_{max} = 43,8" tc rgb "red" font ",12"
set label at 1.92,50 "◼ H = 50%" tc rgb "dark-green" font ",12"
set label at 1.92,80.02 "◼ R(∞) = 80%" tc rgb "blue" font ",12"
set label at 1.92,91.84 "◼ t_{0.1%} = 91,8" tc rgb "black" font ",12"

plot 'Data_R0.csv' u 1:($3*100) w l ls 1 lc rgb "red" ti 'I_{max}',\
    '' u 1:2 w l lc rgb "red" dashtype 2 axes x1y2 ti 't_{max}',\
    '' u 1:($4*100) w l lc rgb "dark-green" ti "H",\
    '' u 1:(100-$5*100) w l lc rgb "blue" ti "R(∞)",\
    '' u 1:6 w l lc rgb "black" dashtype 2 axes x1y2 ti 't_{0.1%}'
