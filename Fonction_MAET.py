# Calcul Mean Annuel Epilimnetic Temperature

def MAET(lat, alt, cont):
    p1 = (750 / (90 - (lat**0.85)))**1.29
    p2 = 0.1 * (alt**0.5)
    p3 = 0.25 * ((cont**0.9) + 500)**0.52
    maet = 44 - p1 - p2 -p3
    print(f"La température moyenne annuelle à l'épilimnion est {maet} °C.")
    return 

LAT = 46.4582030333122746
ALT = 371.8
CONT = 2.8975

MAET(LAT, ALT, CONT)

LAT_MORGES = 46.506314177173326
ALT_MORGES = 371.8
CONT_MORGES = 0.12108

MAET(LAT_MORGES, ALT_MORGES, CONT_MORGES)