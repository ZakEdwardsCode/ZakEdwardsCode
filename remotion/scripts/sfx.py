import numpy as np, scipy.io.wavfile as wf, scipy.signal as ss, sys, os
SR = 48000
out = sys.argv[1]
rng = np.random.default_rng(7)
def t(d): return np.arange(int(SR*d))/SR
def env(n, a, d):  # attack/decay in seconds
    e = np.ones(n); A = int(SR*a); D = int(SR*d)
    if A: e[:A] = np.linspace(0, 1, A)
    if D: e[-D:] *= np.linspace(1, 0, D) ** 2
    return e
def save(name, x, gain=0.8):
    x = x / (np.max(np.abs(x)) + 1e-9) * gain
    st = np.stack([x, x], 1)
    wf.write(os.path.join(out, name), SR, (st * 32767).astype(np.int16))

# whoosh: band-passed noise sweeping up then down, with stereo-ish swell
d = 0.55; n = int(SR*d); noise = rng.standard_normal(n)
x = np.zeros(n); chunks = 40
for i in range(chunks):
    a, b = i*n//chunks, (i+1)*n//chunks
    f = 400 + 3000*np.sin(np.pi*i/chunks)
    sos = ss.butter(2, [f*0.6, f*1.4], btype='band', fs=SR, output='sos')
    x[a:b] = ss.sosfilt(sos, noise[a:b])
x *= np.sin(np.pi*np.linspace(0, 1, n))**1.5
save('whoosh.wav', x, 0.55)

# pop: quick pitch-dropping sine blip
tt = t(0.09); f = 900*np.exp(-tt*35)+300
x = np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-tt*45)
save('pop.wav', x, 0.6)

# click: UI mouse click (two tiny transients)
tt = t(0.05); x = rng.standard_normal(len(tt)) * np.exp(-tt*600)
x = ss.sosfilt(ss.butter(2, 2500, btype='high', fs=SR, output='sos'), x)
x[int(0.018*SR):] += 0.5*x[:len(x)-int(0.018*SR)]
save('click.wav', x, 0.7)

# ding: bell with inharmonic partials
tt = t(1.4); x = sum(a*np.sin(2*np.pi*f*tt)*np.exp(-tt*k) for f, a, k in [(1318.5,1,3),(2637,0.4,5),(3950,0.2,8),(1760,0.25,4)])
x *= env(len(tt), 0.003, 0.05)
save('ding.wav', x, 0.45)

# impact: low boom + noise crack for big statements
tt = t(1.0); f = 120*np.exp(-tt*6)+40
boom = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*4)
crack = ss.sosfilt(ss.butter(2, 1500, fs=SR, output='sos'), rng.standard_normal(len(tt)))*np.exp(-tt*25)
save('impact.wav', boom + 0.3*crack, 0.75)

# riser: rising filtered noise + tone into a reveal
d = 1.2; tt = t(d); f = 200*np.exp(tt*2.2)
tone = np.sin(2*np.pi*np.cumsum(f)/SR)*0.3
nz = ss.sosfilt(ss.butter(2, 3000, btype='high', fs=SR, output='sos'), rng.standard_normal(len(tt)))*0.5
x = (tone + nz) * (tt/d)**2 * env(len(tt), 0, 0.03)
save('riser.wav', x, 0.4)

# chime: success arpeggio (C E G C)
parts = []
for i, f in enumerate([1046.5, 1318.5, 1568, 2093]):
    tt = t(0.6); tone = (np.sin(2*np.pi*f*tt) + 0.3*np.sin(4*np.pi*f*tt))*np.exp(-tt*6)
    pad = np.zeros(int(i*0.08*SR)); parts.append(np.concatenate([pad, tone]))
L = max(map(len, parts)); x = sum(np.pad(p, (0, L-len(p))) for p in parts)
save('chime.wav', x, 0.45)

# tick: soft typewriter/keyboard tick for list items
tt = t(0.03); x = rng.standard_normal(len(tt))*np.exp(-tt*900)
x = ss.sosfilt(ss.butter(2, [2000, 7000], btype='band', fs=SR, output='sos'), x)
save('tick.wav', x, 0.5)

# swoosh (short) for layout transitions
d = 0.3; n = int(SR*d); noise = rng.standard_normal(n)
sos = ss.butter(2, [800, 6000], btype='band', fs=SR, output='sos')
x = ss.sosfilt(sos, noise) * np.sin(np.pi*np.linspace(0,1,n))**2
save('swoosh.wav', x, 0.4)
print(sorted(os.listdir(out)))
