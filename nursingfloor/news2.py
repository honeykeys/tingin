def score_news2(hr: int, rr: int, o2_sat: int, sbp: int, temp: float, consciousness: str = "A") -> int:
    # Respiratory rate
    if rr <= 8:
        rr_s = 3
    elif rr <= 11:
        rr_s = 1
    elif rr <= 20:
        rr_s = 0
    elif rr <= 24:
        rr_s = 2
    else:
        rr_s = 3

    # SpO2 Scale 1
    if o2_sat <= 91:
        spo2_s = 3
    elif o2_sat <= 93:
        spo2_s = 2
    elif o2_sat <= 95:
        spo2_s = 1
    else:
        spo2_s = 0

    # Systolic BP
    if sbp <= 90:
        sbp_s = 3
    elif sbp <= 100:
        sbp_s = 2
    elif sbp <= 110:
        sbp_s = 1
    elif sbp <= 219:
        sbp_s = 0
    else:
        sbp_s = 3

    # Heart rate
    if hr <= 40:
        hr_s = 3
    elif hr <= 50:
        hr_s = 1
    elif hr <= 90:
        hr_s = 0
    elif hr <= 110:
        hr_s = 1
    elif hr <= 130:
        hr_s = 2
    else:
        hr_s = 3

    # Consciousness (AVPU: A=0, anything else=3)
    con_s = 0 if consciousness == "A" else 3

    # Temperature
    if temp <= 35.0:
        temp_s = 3
    elif temp <= 36.0:
        temp_s = 1
    elif temp <= 38.0:
        temp_s = 0
    elif temp <= 39.0:
        temp_s = 1
    else:
        temp_s = 2

    return rr_s + spo2_s + sbp_s + hr_s + con_s + temp_s


def score_news2_from_vitals(v: dict) -> int:
    return score_news2(
        hr=v.get("hr", 80),
        rr=v.get("rr", 16),
        o2_sat=v.get("o2_sat", 97),
        sbp=v.get("sbp", 120),
        temp=v.get("temp", 36.8),
        consciousness=v.get("consciousness", "A"),
    )
