set term pdfcairo enhanced dashed font 'Helvetica,14' size 12cm,10cm dashed
set output "deriv_R.pdf"

unset key

set xrange [0:150]
set yrange [0:100]

set ylabel "Guéris (%)"
set xlabel "Unité de temps"

R(t,g,tp,Ip,Rp)=100*(Rp+g*Ip*(t-tp))


g=.1
Ip=0.0602	
Rp=0.0576
t=20
set arrow from t,0 to t,R(t,g,t,Ip,Rp) nohead lc rgb "grey" dashtype 2
set arrow from t-5,R(t-5,g,t,Ip,Rp) to t+5,R(t+5,g,t,Ip,Rp) nohead lc rgb "black" lw 2 front
set label at t+5,R(t,g,t,Ip,Rp) sprintf("dR/dt=%.2f\%",100*g*Ip) tc rgb "black" font ",12"

Ip=0.1503	
Rp=0.4369
t=50
set arrow from t,0 to t,R(t,g,t,Ip,Rp) nohead lc rgb "grey" dashtype 2
set arrow from t-5,R(t-5,g,t,Ip,Rp) to t+5,R(t+5,g,t,Ip,Rp) nohead lc rgb "black" lw 2 front
set label at t-2,R(t,g,t,Ip,Rp) right sprintf("dR/dt=%.2f\%",100*g*Ip) tc rgb "black" font ",12"

Ip=0.0445		
Rp=0.7224
t=80
set arrow from t,0 to t,R(t,g,t,Ip,Rp) nohead lc rgb "grey" dashtype 2
set arrow from t-5,R(t-5,g,t,Ip,Rp) to t+5,R(t+5,g,t,Ip,Rp) nohead lc rgb "black" lw 2 front
set label at t-2,R(t,g,t,Ip,Rp)+2 right sprintf("dR/dt=%.2f\%",100*g*Ip) tc rgb "black" font ",12"

Ip=0.0044			
Rp=0.7934
t=120
set arrow from t,0 to t,R(t,g,t,Ip,Rp) nohead lc rgb "grey" dashtype 2
set arrow from t-5,R(t-5,g,t,Ip,Rp) to t+5,R(t+5,g,t,Ip,Rp) nohead lc rgb "black" lw 2 front
set label at t,R(t,g,t,Ip,Rp)+5 center sprintf("dR/dt=%.2f\%",100*g*Ip) tc rgb "black" font ",12"


plot 'SIR_R0=2.csv' u ($1):($4*100) w l lc rgb "dark-green" notitle, '' every 10::11 u ($1):($4*100) w p pt 5 ps .5 lc rgb "dark-green"


set output "deriv_I.pdf"

unset arrow
unset label

set yrange [0:20]
set ylabel "Infectés (%)"


b=.2
I(t,b,g,tp,Sp,Ip)=100*(Ip+(b*Sp*Ip-g*Ip)*(t-tp))

Sp=0.8822
Ip=0.0602
t=20
set arrow from t,0 to t,I(t,b,g,t,Sp,Ip) nohead lc rgb "grey" dashtype 2
set arrow from t-5,I(t-5,b,g,t,Sp,Ip) to t+5,I(t+5,b,g,t,Sp,Ip) nohead lc rgb "black" lw 2 front
set label at t+5,I(t,b,g,t,Sp,Ip) sprintf("dI/dt=%.2f\%",(b*Sp*Ip-g*Ip)*100) tc rgb "black" font ",12"

Sp=0.5648	
Ip=0.1549
t=40
set arrow from t,0 to t,I(t,b,g,t,Sp,Ip) nohead lc rgb "grey" dashtype 2
set arrow from t-5,I(t-5,b,g,t,Sp,Ip) to t+5,I(t+5,b,g,t,Sp,Ip) nohead lc rgb "black" lw 2 front
set label at t-2,I(t,b,g,t,Sp,Ip) right sprintf("dI/dt=%.2f\%",(b*Sp*Ip-g*Ip)*100) tc rgb "black" font ",12"

Sp=0.4127	
Ip=0.1503	
t=50
set arrow from t,0 to t,I(t,b,g,t,Sp,Ip) nohead lc rgb "grey" dashtype 2
set arrow from t-5,I(t-5,b,g,t,Sp,Ip) to t+5,I(t+5,b,g,t,Sp,Ip) nohead lc rgb "black" lw 2 front
set label at t+5,I(t,b,g,t,Sp,Ip) sprintf("dI/dt=%.2f\%",(b*Sp*Ip-g*Ip)*100) tc rgb "black" font ",12"

Sp=0.2047		
Ip=0.0080	
t=110
set arrow from t,0 to t,I(t,b,g,t,Sp,Ip) nohead lc rgb "grey" dashtype 2
set arrow from t-5,I(t-5,b,g,t,Sp,Ip) to t+5,I(t+5,b,g,t,Sp,Ip) nohead lc rgb "black" lw 2 front
set label at t+10,I(t,b,g,t,Sp,Ip)+.75 center sprintf("dI/dt=%.2f\%",(b*Sp*Ip-g*Ip)*100) tc rgb "black" font ",12"

Sp=0.2620	
Ip=0.0741
t=70
set arrow from t,0 to t,I(t,b,g,t,Sp,Ip) nohead lc rgb "grey" dashtype 2
set arrow from t-5,I(t-5,b,g,t,Sp,Ip) to t+5,I(t+5,b,g,t,Sp,Ip) nohead lc rgb "black" lw 2 front
set label at t+5,I(t,b,g,t,Sp,Ip) sprintf("dI/dt=%.2f\%",(b*Sp*Ip-g*Ip)*100) tc rgb "black" font ",12"

plot 'SIR_R0=2.csv' u ($1):($3*100) w l lc rgb "red" notitle, '' every 10::11 u ($1):($3*100) w p pt 5 ps .5 lc rgb "red"

