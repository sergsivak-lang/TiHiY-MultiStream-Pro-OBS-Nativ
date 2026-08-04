from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np
import wave, math, random, sys

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('work/assets')
FONT_PATH = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('work/fonts/Tektur.ttf')
OUT.mkdir(parents=True, exist_ok=True)
W, H = 2560, 1440
SCENE_DUR = 5.2
XFADE = 0.35
SCENES = 12
TOTAL = SCENE_DUR * SCENES - XFADE * (SCENES - 1)
STEP = SCENE_DUR - XFADE

voice_ua = [
    '2956 рік. Ми дісталися зірок.',
    'Та космос так і не став безпечним.',
    'Там, де закінчується закон, починається справжній фронтир.',
    'Контракти. Ризик. Вогонь. Невідомі світи.',
    'Ми летимо туди, куди інші не наважуються.',
    'Корабель — наш дім. Екіпаж — наша сила.',
    'А порожнеча між зірками — наше поле бою.',
    'Ми втрачали кораблі. Падали. І знову поверталися.',
    'Бо кожен бій залишає шрам. Кожен політ — історію.',
    'Ми не спостерігаємо за всесвітом.',
    'Ми залишаємо в ньому свій слід.'
]

caption_ua = [
    '2956 РІК.\nМИ ДІСТАЛИСЯ ЗІРОК.',
    'ТА КОСМОС ТАК І НЕ СТАВ\nБЕЗПЕЧНИМ.',
    'ТАМ, ДЕ ЗАКІНЧУЄТЬСЯ ЗАКОН,\nПОЧИНАЄТЬСЯ СПРАВЖНІЙ ФРОНТИР.',
    'КОНТРАКТИ. РИЗИК. ВОГОНЬ.\nНЕВІДОМІ СВІТИ.',
    'МИ ЛЕТИМО ТУДИ,\nКУДИ ІНШІ НЕ НАВАЖУЮТЬСЯ.',
    'КОРАБЕЛЬ — НАШ ДІМ.\nЕКІПАЖ — НАША СИЛА.',
    'ПОРОЖНЕЧА МІЖ ЗІРКАМИ —\nНАШЕ ПОЛЕ БОЮ.',
    'МИ ВТРАЧАЛИ КОРАБЛІ. ПАДАЛИ.\nІ ЗНОВУ ПОВЕРТАЛИСЯ.',
    'КОЖЕН БІЙ ЗАЛИШАЄ ШРАМ.\nКОЖЕН ПОЛІТ — ІСТОРІЮ.',
    'МИ НЕ СПОСТЕРІГАЄМО\nЗА ВСЕСВІТОМ.',
    'МИ ЗАЛИШАЄМО В НЬОМУ\nСВІЙ СЛІД.'
]

caption_en = [
    '2956. WE REACHED THE STARS.',
    'BUT SPACE NEVER BECAME SAFE.',
    'WHERE THE LAW ENDS, THE TRUE FRONTIER BEGINS.',
    'CONTRACTS. RISK. FIRE. UNKNOWN WORLDS.',
    'WE FLY WHERE OTHERS DARE NOT.',
    'OUR SHIP IS HOME. OUR CREW IS STRENGTH.',
    'THE VOID BETWEEN THE STARS IS OUR BATTLEFIELD.',
    'WE LOST SHIPS. WE FELL. AND WE CAME BACK.',
    'EVERY BATTLE LEAVES A SCAR. EVERY FLIGHT, A STORY.',
    'WE DO NOT WATCH THE UNIVERSE.',
    'WE LEAVE OUR MARK ON IT.'
]

for i, text in enumerate(voice_ua, 1):
    (OUT / f'voice_{i:02d}.txt').write_text(text, encoding='utf-8')


def get_font(size, weight=850):
    f = ImageFont.truetype(str(FONT_PATH), size=size)
    try:
        axes = f.get_variation_axes()
        if len(axes) >= 2:
            f.set_variation_by_axes([100, weight])
        elif len(axes) == 1:
            f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def text_mask(text, font, y_center, spacing=12, max_width=2260):
    mask = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(mask)
    lines = text.split('\n')
    boxes = [d.textbbox((0,0), line, font=font, stroke_width=0) for line in lines]
    widths = [b[2]-b[0] for b in boxes]
    heights = [b[3]-b[1] for b in boxes]
    total_h = sum(heights) + spacing * (len(lines)-1)
    y = int(y_center - total_h/2)
    for line, ww, hh in zip(lines, widths, heights):
        x = int((W-ww)/2)
        d.text((x,y), line, fill=255, font=font, stroke_width=0)
        y += hh + spacing
    return mask


def metallic_layer(mask, seed, cold=False):
    rng = np.random.default_rng(seed)
    yy = np.linspace(0, 1, H)[:,None]
    top = np.array([245,248,250], dtype=np.float32)
    bot = np.array([82,91,98], dtype=np.float32)
    grad = top[None,None,:]*(1-yy[:,:,None]) + bot[None,None,:]*yy[:,:,None]
    grad = np.repeat(grad, W, axis=1)
    noise = rng.normal(0, 12, (H,W,1))
    brushed = rng.normal(0, 6, (H,1,1))
    arr = np.clip(grad + noise + brushed, 0, 255).astype(np.uint8)
    tex = Image.fromarray(arr, 'RGB')
    td = ImageDraw.Draw(tex)
    for _ in range(130):
        x = int(rng.integers(120, W-120)); y = int(rng.integers(800, H-80))
        ln = int(rng.integers(12, 110))
        col = tuple(int(v) for v in ((52,58,62) if rng.random() < .72 else (232,238,241)))
        td.line((x,y,x+ln,y+int(rng.integers(-2,3))), fill=col, width=int(rng.integers(1,3)))
    alpha = mask
    rgba = tex.convert('RGBA'); rgba.putalpha(alpha)
    if cold:
        blue = Image.new('RGBA',(W,H),(180,225,255,0)); blue.putalpha(mask.point(lambda p: int(p*.20)))
        rgba = Image.alpha_composite(rgba, blue)
    return rgba


def render_caption(idx, ua, en):
    canvas = Image.new('RGBA',(W,H),(0,0,0,0))
    ua_font = get_font(84 if len(ua) < 50 else 72, 900)
    en_font = get_font(38, 800)
    ua_mask = text_mask(ua, ua_font, 1130, spacing=8)
    en_mask = text_mask(en, en_font, 1323, spacing=4)

    for mask, blur, alpha in [(ua_mask, 16, 165), (en_mask, 10, 120)]:
        glow = mask.filter(ImageFilter.GaussianBlur(blur))
        cyan = Image.new('RGBA',(W,H),(0,170,255,0)); cyan.putalpha(glow.point(lambda p: int(p*alpha/255)))
        canvas = Image.alpha_composite(canvas, cyan)

    ua_outline = ua_mask.filter(ImageFilter.MaxFilter(13))
    ua_ring = ImageChops.subtract(ua_outline, ua_mask)
    outline_rgba = Image.new('RGBA',(W,H),(6,10,14,0)); outline_rgba.putalpha(ua_ring.point(lambda p: int(p*.96)))
    canvas = Image.alpha_composite(canvas, outline_rgba)
    ua_tex = metallic_layer(ua_mask, 1000+idx, cold=False)
    canvas = Image.alpha_composite(canvas, ua_tex)

    en_outline = en_mask.filter(ImageFilter.MaxFilter(7))
    en_ring = ImageChops.subtract(en_outline, en_mask)
    en_out = Image.new('RGBA',(W,H),(4,8,12,0)); en_out.putalpha(en_ring.point(lambda p: int(p*.92)))
    canvas = Image.alpha_composite(canvas, en_out)
    en_tex = metallic_layer(en_mask, 2000+idx, cold=True)
    canvas = Image.alpha_composite(canvas, en_tex)
    canvas.save(OUT / f'caption_{idx:02d}.png')

for i,(u,e) in enumerate(zip(caption_ua, caption_en),1):
    render_caption(i,u,e)

# Opening title and end brand in the same beaten-steel language.
def render_center(text, filename, size, y=720):
    canvas=Image.new('RGBA',(W,H),(0,0,0,0))
    f=get_font(size,900)
    mask=text_mask(text,f,y,spacing=8)
    glow=mask.filter(ImageFilter.GaussianBlur(22))
    g=Image.new('RGBA',(W,H),(0,185,255,0)); g.putalpha(glow.point(lambda p:int(p*.68)))
    canvas=Image.alpha_composite(canvas,g)
    outer=mask.filter(ImageFilter.MaxFilter(17)); ring=ImageChops.subtract(outer,mask)
    o=Image.new('RGBA',(W,H),(3,7,10,0)); o.putalpha(ring.point(lambda p:int(p*.98)))
    canvas=Image.alpha_composite(canvas,o)
    canvas=Image.alpha_composite(canvas, metallic_layer(mask, 555, cold=False))
    canvas.save(OUT/filename)

render_center('STAR CITIZEN','title.png',178,720)
render_center('TiHiY-DED','brand.png',168,720)

# Procedural driving cinematic music bed.
sr=48000
dur=TOTAL
t=np.arange(int(sr*dur))/sr
L=np.zeros_like(t); R=np.zeros_like(t)
rng=np.random.default_rng(2956)

# Dark minor pad progression (D minor - Bb - F - C).
chords=[(73.42,87.31,110.0),(58.27,73.42,87.31),(87.31,110.0,130.81),(65.41,82.41,98.0)]
bar=60/100*4
for bi,start in enumerate(np.arange(0,dur,bar)):
    freqs=chords[(bi//2)%4]
    idx=(t>=start)&(t<min(dur,start+bar))
    tt=t[idx]-start
    env=np.minimum(1,tt/.35)*np.minimum(1,(bar-tt)/.45)
    pad=np.zeros(idx.sum())
    for f in freqs:
        pad += .055*np.sin(2*np.pi*f*tt)+.018*np.sin(2*np.pi*2*f*tt)
    L[idx]+=pad*env; R[idx]+=pad*env

# Low pulse and drums.
beat=60/100
for n,bt in enumerate(np.arange(5.5,dur,beat)):
    idx=(t>=bt)&(t<bt+.42); tt=t[idx]-bt
    kick=np.sin(2*np.pi*(68-42*tt)*tt)*np.exp(-10*tt)
    L[idx]+=.28*kick; R[idx]+=.28*kick
    if n%2==1 and bt>12:
        idx2=(t>=bt)&(t<bt+.20); tt2=t[idx2]-bt
        sn=rng.normal(0,1,idx2.sum())*np.exp(-20*tt2)
        L[idx2]+=.085*sn; R[idx2]+=.10*sn

# Eighth-note metallic pulse from midpoint onward.
for bt in np.arange(18,dur,beat/2):
    idx=(t>=bt)&(t<bt+.16); tt=t[idx]-bt
    f=220*(2**((int(bt/(beat/2))%6)/12))
    tone=(np.sin(2*np.pi*f*tt)+.35*np.sin(2*np.pi*2*f*tt))*np.exp(-18*tt)
    pan=.35*np.sin(bt*.9)
    L[idx]+=.06*tone*(1-pan); R[idx]+=.06*tone*(1+pan)

# Scene-change risers and impacts.
transitions=[STEP*i for i in range(1,SCENES)]
for bt in transitions:
    pre=.72
    idx=(t>=max(0,bt-pre))&(t<bt); tt=t[idx]-(bt-pre)
    env=(tt/pre)**1.6
    noise=rng.normal(0,1,idx.sum())*env
    carrier=np.sin(2*np.pi*(180*tt+250*tt*tt))*env
    L[idx]+=.035*noise+.045*carrier; R[idx]+=.04*noise+.045*carrier
    idx2=(t>=bt)&(t<bt+.5); tt2=t[idx2]-bt
    boom=(np.sin(2*np.pi*48*tt2)+.45*np.sin(2*np.pi*72*tt2))*np.exp(-7*tt2)
    grit=rng.normal(0,1,idx2.sum())*np.exp(-16*tt2)
    L[idx2]+=.28*boom+.04*grit; R[idx2]+=.28*boom+.04*grit

# Final braam.
for bt in [0.3, 24.2, 48.5]:
    idx=(t>=bt)&(t<min(dur,bt+2.8)); tt=t[idx]-bt
    br=(np.sin(2*np.pi*43.65*tt)+.5*np.sin(2*np.pi*65.4*tt)+.24*np.sin(2*np.pi*87.3*tt))*np.exp(-1.0*tt)
    L[idx]+=.16*br; R[idx]+=.16*br

# Subtle stereo atmosphere.
wind=rng.normal(0,1,len(t))*.015
L+=wind+0.012*np.sin(2*np.pi*.09*t)
R+=np.roll(wind,240)+0.012*np.sin(2*np.pi*.11*t+.7)

# Dynamic arc.
arc=np.ones_like(t)
arc[t<5]=np.linspace(.35,1,(t<5).sum())
arc[(t>=38)&(t<46)]*=1.12
arc[t>54]*=np.linspace(1,.52,(t>54).sum())
L*=arc; R*=arc
st=np.stack([L,R],axis=1)
peak=np.max(np.abs(st)); st=st/(peak/0.92)
pcm=(st*32767).astype(np.int16)
with wave.open(str(OUT/'music.wav'),'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes(pcm.tobytes())

(OUT/'timing.txt').write_text('\n'.join([f'{i+1:02d} {i*STEP+0.45:.3f}' for i in range(11)]), encoding='utf-8')
print(f'assets ready, total duration {TOTAL:.3f}s')
