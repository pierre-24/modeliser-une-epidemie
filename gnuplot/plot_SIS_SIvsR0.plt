set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "SI_R0.pdf"
set multiplot

set key above

set ylabel "Susceptible (%)"
set xlabel "Infectés (%)"

I(S, R0, S0) = 1-S0 + (1./(S0*R0)-1)*(S-S0)
#-log(S0)/R0 + (1./R0-1)*(S-1)

set label at  (1./1.5)*100,9 center "I_{max} = 6.9%" tc rgb "red" font ",12"
set label at  46,2 left "S(∞)=40%" tc rgb "red" font ",12"

set label at  (1./2)*100,18 center "I_{max} = 15.8%" tc rgb "dark-green" font ",12"
set label at  22,2 left "S(∞)=20%" tc rgb "dark-green" font ",12"

set label at  (1./3)*100,32 center "I_{max} = 30.3%" tc rgb "blue" font ",12"
set label at  7,2 left "S(∞)=6%" tc rgb "blue" font ",12"

set label at  (1./4)*100,42 center "I_{max} = 40.6%" tc rgb "black" font ",12"

plot 'SIR_R0=1.5.csv' u ($2*100):($3*100) w l lc rgb "red" ti "{/Symbol b}=15%",\
     'SIR_R0=2.csv' u ($2*100):($3*100) w l lc rgb "dark-green" ti "{/Symbol b}=20%",\
     'SIR_R0=3.csv' u ($2*100):($3*100) w l lc rgb "blue" ti "{/Symbol b}=30%",\
     'SIR_R0=4.csv' u ($2*100):($3*100) w l lc rgb "black" ti "{/Symbol b}=40%"
