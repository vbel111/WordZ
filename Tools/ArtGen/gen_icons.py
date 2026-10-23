"""Original Word Z icon set: chunky cartoon icons with a dark-brown outline, rendered later by render.js."""
import os

OUT = os.path.join(os.path.dirname(__file__), 'svg')
OL = '#4A2410'   # outline
SW = 7           # stroke width at 256px

DEFS = f'''
<defs>
  <filter id="ds" x="-20%" y="-20%" width="140%" height="150%">
    <feDropShadow dx="0" dy="6" stdDeviation="3" flood-color="#2a1205" flood-opacity="0.35"/>
  </filter>
  <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFE45A"/><stop offset="1" stop-color="#F5A511"/></linearGradient>
  <linearGradient id="goldDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0A21A"/><stop offset="1" stop-color="#C77306"/></linearGradient>
  <linearGradient id="wood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98A4E"/><stop offset="1" stop-color="#9A5B27"/></linearGradient>
  <linearGradient id="woodDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8F5124"/><stop offset="1" stop-color="#6A3714"/></linearGradient>
  <linearGradient id="red" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF6B5E"/><stop offset="1" stop-color="#D93636"/></linearGradient>
  <linearGradient id="green" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8BE05A"/><stop offset="1" stop-color="#3FA52A"/></linearGradient>
  <linearGradient id="blue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6CC8FF"/><stop offset="1" stop-color="#2584E0"/></linearGradient>
  <linearGradient id="purple" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C98BFF"/><stop offset="1" stop-color="#7B2FD6"/></linearGradient>
  <linearGradient id="cream" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFBEF"/><stop offset="1" stop-color="#F0DDB8"/></linearGradient>
  <linearGradient id="grey" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2F4F8"/><stop offset="1" stop-color="#B9C2D0"/></linearGradient>
  <linearGradient id="pink" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9EC0"/><stop offset="1" stop-color="#E8508A"/></linearGradient>
  <linearGradient id="orange" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFB45E"/><stop offset="1" stop-color="#EE7A1E"/></linearGradient>
  <linearGradient id="teal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6FE3D6"/><stop offset="1" stop-color="#1FA89B"/></linearGradient>
  <linearGradient id="dark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5A6478"/><stop offset="1" stop-color="#2D3444"/></linearGradient>
  <radialGradient id="shine" cx="0.35" cy="0.3" r="0.6"><stop offset="0" stop-color="#fff" stop-opacity="0.75"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
</defs>'''


def svg(w, h, body, defs=DEFS):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs}{body}</svg>'


BODIES = {}


def icon(name, body, size=256):
    BODIES[name] = body
    os.makedirs(OUT, exist_ok=True)
    s = svg(256, 256, f'<g filter="url(#ds)" stroke="{OL}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round">{body}</g>')
    if size != 256:
        s = s.replace('width="256" height="256"', f'width="{size}" height="{size}"', 1)
    open(os.path.join(OUT, f'icon_{name}.svg'), 'w').write(s)


HL = 'stroke="none" fill="#fff" fill-opacity="0.45"'   # highlight blob style

# ---------------- currencies & rewards ----------------
icon('coin', f'''
<circle cx="128" cy="128" r="100" fill="url(#goldDark)"/>
<circle cx="128" cy="122" r="84" fill="url(#gold)"/>
<circle cx="128" cy="122" r="62" fill="none" stroke="#E09812" stroke-width="8"/>
<path d="M128 78 L141 108 L173 110 L148 130 L157 162 L128 144 L99 162 L108 130 L83 110 L115 108 Z" fill="#F2AC1E" stroke="#C77306" stroke-width="5"/>
<ellipse cx="96" cy="84" rx="26" ry="14" transform="rotate(-30 96 84)" {HL}/>''')

icon('gem', f'''
<path d="M128 230 L230 104 L186 44 L70 44 L26 104 Z" fill="url(#purple)"/>
<path d="M26 104 L230 104" fill="none"/>
<path d="M70 44 L98 104 L128 44 L158 104 L186 44" fill="none" stroke-width="5"/>
<path d="M98 104 L128 230 L158 104" fill="none" stroke-width="5"/>
<path d="M70 44 L128 44 L98 104 L26 104 Z" fill="#E2C2FF" stroke="none" opacity="0.7"/>
<path d="M128 44 L186 44 L158 104 Z" fill="#fff" stroke="none" opacity="0.35"/>
<ellipse cx="80" cy="70" rx="14" ry="8" transform="rotate(-30 80 70)" {HL}/>''')

icon('star', f'''
<path d="M128 22 L158 92 L234 98 L176 148 L194 224 L128 184 L62 224 L80 148 L22 98 L98 92 Z" fill="url(#gold)"/>
<path d="M128 52 L148 100 L200 104 L160 138" fill="none" stroke="#fff" stroke-opacity="0.6" stroke-width="8"/>''')

icon('chest', f'''
<rect x="30" y="112" width="196" height="112" rx="16" fill="url(#wood)"/>
<path d="M30 118 Q30 40 128 40 Q226 40 226 118 Z" fill="url(#woodDark)"/>
<rect x="30" y="104" width="196" height="26" rx="8" fill="url(#gold)"/>
<rect x="56" y="44" width="22" height="180" fill="url(#gold)"/>
<rect x="178" y="44" width="22" height="180" fill="url(#gold)"/>
<rect x="106" y="102" width="44" height="54" rx="10" fill="url(#gold)"/>
<circle cx="128" cy="124" r="8" fill="{OL}" stroke="none"/>
<path d="M60 70 Q100 52 140 56" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="10"/>''')

icon('chest_purple', f'''
<rect x="30" y="112" width="196" height="112" rx="16" fill="url(#purple)"/>
<path d="M30 118 Q30 40 128 40 Q226 40 226 118 Z" fill="#6A22BE"/>
<rect x="30" y="104" width="196" height="26" rx="8" fill="url(#gold)"/>
<rect x="56" y="44" width="22" height="180" fill="url(#gold)"/>
<rect x="178" y="44" width="22" height="180" fill="url(#gold)"/>
<rect x="106" y="102" width="44" height="54" rx="10" fill="url(#gold)"/>
<circle cx="128" cy="124" r="8" fill="{OL}" stroke="none"/>
<path d="M60 70 Q100 52 140 56" fill="none" stroke="#fff" stroke-opacity="0.35" stroke-width="10"/>''')

icon('sad', f'''
<circle cx="128" cy="128" r="104" fill="url(#gold)"/>
<ellipse cx="90" cy="112" rx="14" ry="20" fill="{OL}" stroke="none"/>
<ellipse cx="166" cy="112" rx="14" ry="20" fill="{OL}" stroke="none"/>
<path d="M72 94 L104 80" fill="none" stroke-width="8"/><path d="M184 94 L152 80" fill="none" stroke-width="8"/>
<path d="M82 182 Q128 140 174 182" fill="none" stroke-width="10"/>
<ellipse cx="86" cy="64" rx="30" ry="16" transform="rotate(-30 86 64)" {HL}/>''')

icon('avatar', f'''
<circle cx="128" cy="128" r="108" fill="url(#blue)"/>
<circle cx="128" cy="104" r="40" fill="url(#cream)"/>
<path d="M58 206 Q64 150 128 150 Q192 150 198 206 Q160 236 128 236 Q96 236 58 206 Z" fill="url(#cream)"/>''')

# ---------------- hint / booster icons ----------------
icon('bulb', f'''
<path d="M128 24 C76 24 46 64 50 104 C54 140 86 152 92 178 L164 178 C170 152 202 140 206 104 C210 64 180 24 128 24 Z" fill="url(#gold)"/>
<rect x="90" y="176" width="76" height="24" rx="8" fill="url(#grey)"/>
<rect x="96" y="198" width="64" height="22" rx="8" fill="url(#grey)"/>
<path d="M110 222 L146 222 L138 236 L118 236 Z" fill="#7B8496"/>
<path d="M104 152 L116 128 L128 152 L140 128 L152 152" fill="none" stroke="#E08A0E" stroke-width="7"/>
<ellipse cx="96" cy="70" rx="22" ry="14" transform="rotate(-35 96 70)" {HL}/>''')

icon('shuffle', f'''
<path d="M30 76 L82 76 Q110 76 128 128 Q146 180 174 180 L196 180" fill="none" stroke="#fff" stroke-width="30"/>
<path d="M30 180 L82 180 Q110 180 128 128 Q146 76 174 76 L196 76" fill="none" stroke="#fff" stroke-width="30"/>
<path d="M30 76 L82 76 Q110 76 128 128 Q146 180 174 180 L196 180" fill="none" stroke="url(#purple)" stroke-width="16"/>
<path d="M30 180 L82 180 Q110 180 128 128 Q146 76 174 76 L196 76" fill="none" stroke="url(#purple)" stroke-width="16"/>
<path d="M190 44 L238 76 L190 108 Z" fill="#B067F5"/>
<path d="M190 148 L238 180 L190 212 Z" fill="#B067F5"/>''')

icon('magnifier', f'''
<path d="M150 150 L222 222" stroke-width="40"/>
<path d="M150 150 L222 222" stroke="url(#woodDark)" stroke-width="26"/>
<circle cx="104" cy="104" r="78" fill="#BFE9FF"/>
<circle cx="104" cy="104" r="78" fill="none" stroke="url(#blue)" stroke-width="22"/>
<circle cx="104" cy="104" r="78" fill="none"/>
<path d="M66 84 Q76 58 104 52" fill="none" stroke="#fff" stroke-width="12"/>''')

icon('clock', f'''
<rect x="110" y="8" width="36" height="26" rx="6" fill="url(#red)"/>
<circle cx="128" cy="140" r="100" fill="url(#red)"/>
<circle cx="128" cy="140" r="78" fill="url(#cream)"/>
<path d="M128 140 L128 90" stroke-width="12"/><path d="M128 140 L164 158" stroke-width="12"/>
<circle cx="128" cy="140" r="9" fill="{OL}"/>
<ellipse cx="84" cy="84" rx="24" ry="12" transform="rotate(-35 84 84)" {HL}/>''')

icon('letter', f'''
<rect x="34" y="34" width="188" height="188" rx="36" fill="url(#cream)"/>
<text x="128" y="186" font-family="Baloo" font-size="170" text-anchor="middle" fill="#7A4A1E" stroke="none">A</text>
<path d="M190 30 L204 58 L234 62 L212 82 L218 112 L190 98 L162 112 L168 82 L146 62 L176 58 Z" fill="url(#gold)" stroke-width="5"/>''')

icon('wand', f'''
<path d="M54 210 L170 94" stroke-width="34"/>
<path d="M54 210 L170 94" stroke="url(#woodDark)" stroke-width="20"/>
<path d="M150 112 L176 86" stroke="#fff" stroke-width="20"/>
<path d="M186 22 L198 56 L234 58 L206 80 L216 114 L186 94 L156 114 L166 80 L138 58 L174 56 Z" fill="url(#gold)" stroke-width="6"/>
<circle cx="80" cy="70" r="10" fill="#fff" stroke-width="4"/><circle cx="216" cy="166" r="8" fill="#fff" stroke-width="4"/>''')

# ---------------- navigation / dock ----------------
icon('home', f'''
<path d="M24 128 L128 34 L232 128 Z" fill="url(#red)"/>
<rect x="56" y="118" width="144" height="104" rx="10" fill="url(#cream)"/>
<rect x="106" y="152" width="44" height="70" rx="8" fill="url(#wood)"/>
<rect x="164" y="56" width="26" height="46" fill="url(#woodDark)"/>''')

icon('replay', f'''
<path d="M196 128 A68 68 0 1 1 156 66" fill="none" stroke-width="44"/>
<path d="M196 128 A68 68 0 1 1 156 66" fill="none" stroke="url(#green)" stroke-width="28"/>
<path d="M140 26 L214 54 L150 106 Z" fill="url(#green)"/>''')

icon('share', f'''
<path d="M70 128 L184 64 M70 128 L184 192" stroke-width="30"/>
<path d="M70 128 L184 64 M70 128 L184 192" stroke="url(#blue)" stroke-width="16"/>
<circle cx="70" cy="128" r="40" fill="url(#blue)"/>
<circle cx="184" cy="62" r="38" fill="url(#blue)"/>
<circle cx="184" cy="194" r="38" fill="url(#blue)"/>''')

icon('calendar', f'''
<rect x="28" y="46" width="200" height="182" rx="22" fill="url(#cream)"/>
<path d="M28 68 Q28 46 50 46 L206 46 Q228 46 228 68 L228 104 L28 104 Z" fill="url(#red)"/>
<rect x="66" y="22" width="22" height="50" rx="10" fill="url(#grey)"/><rect x="168" y="22" width="22" height="50" rx="10" fill="url(#grey)"/>
<g stroke="none" fill="#E3B26B"><rect x="56" y="124" width="34" height="30" rx="6"/><rect x="111" y="124" width="34" height="30" rx="6"/><rect x="166" y="124" width="34" height="30" rx="6"/>
<rect x="56" y="170" width="34" height="30" rx="6"/><rect x="166" y="170" width="34" height="30" rx="6"/></g>
<rect x="111" y="170" width="34" height="30" rx="6" fill="#4CC23A" stroke-width="4"/>''')

icon('trophy', f'''
<path d="M70 40 L186 40 L182 112 Q176 160 128 164 Q80 160 74 112 Z" fill="url(#gold)"/>
<path d="M74 60 Q30 60 34 96 Q38 130 82 132" fill="none" stroke-width="16"/>
<path d="M74 60 Q30 60 34 96 Q38 130 82 132" fill="none" stroke="#F5B21A" stroke-width="6"/>
<path d="M182 60 Q226 60 222 96 Q218 130 174 132" fill="none" stroke-width="16"/>
<path d="M182 60 Q226 60 222 96 Q218 130 174 132" fill="none" stroke="#F5B21A" stroke-width="6"/>
<rect x="112" y="162" width="32" height="30" fill="url(#goldDark)"/>
<rect x="70" y="190" width="116" height="40" rx="10" fill="url(#woodDark)"/>
<path d="M100 60 Q100 120 128 140" fill="none" stroke="#fff" stroke-opacity="0.5" stroke-width="10"/>''')

icon('shop', f'''
<rect x="40" y="104" width="176" height="122" rx="10" fill="url(#cream)"/>
<rect x="128" y="140" width="56" height="86" rx="6" fill="url(#wood)"/>
<rect x="60" y="140" width="50" height="46" rx="6" fill="#BFE9FF"/>
<path d="M26 104 L44 34 L212 34 L230 104 Z" fill="url(#red)"/>
<path d="M26 104 Q48 132 70 104 Q92 132 114 104 Q136 132 158 104 Q180 132 202 104 Q216 124 230 104" fill="url(#red)"/>
<path d="M84 34 L76 104 M128 34 L128 104 M172 34 L180 104" fill="none" stroke="#fff" stroke-width="14"/>''')

icon('quest', f'''
<rect x="58" y="44" width="140" height="172" rx="10" fill="url(#cream)"/>
<rect x="40" y="26" width="176" height="36" rx="18" fill="url(#wood)"/>
<rect x="40" y="198" width="176" height="36" rx="18" fill="url(#wood)"/>
<g stroke-width="8"><path d="M86 96 L170 96"/><path d="M86 128 L170 128"/><path d="M86 160 L140 160"/></g>
<circle cx="190" cy="186" r="30" fill="url(#red)" stroke-width="6"/>''')

icon('gift', f'''
<rect x="36" y="104" width="184" height="122" rx="12" fill="url(#purple)"/>
<rect x="26" y="78" width="204" height="44" rx="10" fill="#B371F7"/>
<rect x="112" y="78" width="32" height="148" fill="url(#gold)"/>
<path d="M128 78 Q88 18 66 48 Q52 76 128 78 Q204 76 190 48 Q168 18 128 78 Z" fill="url(#gold)"/>''')

icon('lock', f'''
<path d="M82 112 L82 82 A46 46 0 0 1 174 82 L174 112" fill="none" stroke-width="40"/>
<path d="M82 112 L82 82 A46 46 0 0 1 174 82 L174 112" fill="none" stroke="url(#grey)" stroke-width="24"/>
<rect x="46" y="108" width="164" height="124" rx="22" fill="url(#gold)"/>
<circle cx="128" cy="158" r="16" fill="{OL}" stroke="none"/><rect x="120" y="164" width="16" height="36" rx="6" fill="{OL}" stroke="none"/>''')

icon('play', f'''<path d="M70 36 Q60 30 60 44 L60 212 Q60 226 72 220 L214 140 Q226 128 214 116 Z" fill="url(#gold)"/>''')
icon('pause', f'''<rect x="52" y="36" width="56" height="184" rx="16" fill="url(#cream)"/><rect x="148" y="36" width="56" height="184" rx="16" fill="url(#cream)"/>''')
icon('restart', f'''
<path d="M196 128 A68 68 0 1 1 156 66" fill="none" stroke-width="44"/>
<path d="M196 128 A68 68 0 1 1 156 66" fill="none" stroke="#fff" stroke-width="28"/>
<path d="M140 26 L214 54 L150 106 Z" fill="#fff"/>''')
icon('exit', f'''
<rect x="40" y="30" width="120" height="196" rx="12" fill="url(#wood)"/>
<rect x="58" y="48" width="84" height="178" fill="url(#woodDark)"/>
<circle cx="126" cy="132" r="8" fill="url(#gold)" stroke-width="4"/>
<path d="M150 128 L210 128" stroke-width="40"/><path d="M150 128 L210 128" stroke="#fff" stroke-width="24"/>
<path d="M196 88 L244 128 L196 168 Z" fill="#fff"/>''')
icon('gear', f'''
<g fill="url(#grey)">
<path d="M112 20 L144 20 L150 52 Q164 56 176 64 L204 46 L226 68 L208 96 Q216 108 220 122 L252 128 L252 128 L220 134 Q216 148 208 160 L226 188 L204 210 L176 192 Q164 200 150 204 L144 236 L112 236 L106 204 Q92 200 80 192 L52 210 L30 188 L48 160 Q40 148 36 134 L4 128 L36 122 Q40 108 48 96 L30 68 L52 46 L80 64 Q92 56 106 52 Z"/></g>
<circle cx="128" cy="128" r="36" fill="#8A93A6"/>''')
icon('back', f'''<path d="M156 54 L80 128 L156 202" fill="none" stroke-width="58"/><path d="M156 54 L80 128 L156 202" fill="none" stroke="#fff" stroke-width="36"/>''')
icon('check', f'''<circle cx="128" cy="128" r="104" fill="url(#green)"/><path d="M76 132 L112 168 L184 92" fill="none" stroke="#fff" stroke-width="26"/>''')
icon('ad', f'''<rect x="22" y="48" width="212" height="152" rx="26" fill="url(#blue)"/><path d="M108 92 L108 156 L164 124 Z" fill="#fff"/><path d="M96 200 L160 200 L172 232 L84 232 Z" fill="url(#grey)"/>''')
icon('bolt', f'''<path d="M150 14 L54 142 L120 142 L98 242 L204 102 L136 102 Z" fill="url(#gold)"/>''')
icon('crown', f'''
<path d="M28 196 L18 70 L82 124 L128 40 L174 124 L238 70 L228 196 Z" fill="url(#gold)"/>
<rect x="28" y="190" width="200" height="34" rx="10" fill="url(#goldDark)"/>
<circle cx="128" cy="150" r="18" fill="url(#red)" stroke-width="5"/>
<circle cx="18" cy="66" r="14" fill="url(#gold)"/><circle cx="128" cy="36" r="14" fill="url(#gold)"/><circle cx="238" cy="66" r="14" fill="url(#gold)"/>''')
icon('leaf_btn', f'''<path d="M128 228 Q30 160 60 60 Q140 20 200 40 Q230 140 128 228 Z" fill="url(#green)"/><path d="M128 220 Q120 120 176 54" fill="none" stroke-width="6"/>''')

# ---------------- category icons ----------------
CAT = {
 'CITY': f'''
<rect x="30" y="104" width="62" height="124" rx="6" fill="url(#orange)"/>
<rect x="96" y="40" width="70" height="188" rx="6" fill="url(#blue)"/>
<rect x="170" y="88" width="56" height="140" rx="6" fill="url(#purple)"/>
<g stroke="none" fill="#FFF3B0"><rect x="44" y="124" width="14" height="16"/><rect x="66" y="124" width="14" height="16"/><rect x="44" y="160" width="14" height="16"/><rect x="66" y="160" width="14" height="16"/>
<rect x="112" y="62" width="14" height="18"/><rect x="138" y="62" width="14" height="18"/><rect x="112" y="102" width="14" height="18"/><rect x="138" y="102" width="14" height="18"/><rect x="112" y="142" width="14" height="18"/><rect x="138" y="142" width="14" height="18"/>
<rect x="184" y="108" width="12" height="16"/><rect x="204" y="108" width="12" height="16"/><rect x="184" y="146" width="12" height="16"/><rect x="204" y="146" width="12" height="16"/></g>
<rect x="18" y="222" width="220" height="16" rx="6" fill="url(#woodDark)"/>''',
 'ELECTRONIC': f'''
<rect x="40" y="46" width="176" height="122" rx="14" fill="url(#dark)"/>
<rect x="56" y="62" width="144" height="90" rx="6" fill="url(#blue)" stroke-width="4"/>
<path d="M18 176 L238 176 L222 214 L34 214 Z" fill="url(#grey)"/>
<rect x="104" y="184" width="48" height="10" rx="5" fill="#8A93A6" stroke="none"/>
<path d="M70 80 Q100 70 130 76" fill="none" stroke="#fff" stroke-opacity="0.6" stroke-width="8"/>''',
 'THINGS': None,  # bulb
 'MEALS': f'''
<path d="M30 110 Q30 40 128 40 Q226 40 226 110 Z" fill="url(#orange)"/>
<g stroke="none" fill="#FFF3D0"><ellipse cx="90" cy="70" rx="7" ry="4"/><ellipse cx="128" cy="58" rx="7" ry="4"/><ellipse cx="166" cy="72" rx="7" ry="4"/><ellipse cx="112" cy="88" rx="7" ry="4"/><ellipse cx="150" cy="92" rx="7" ry="4"/></g>
<path d="M22 120 Q60 104 90 122 Q128 104 166 122 Q200 104 234 120 L230 136 L26 136 Z" fill="url(#green)"/>
<rect x="24" y="134" width="208" height="30" rx="12" fill="#8B3E1A"/>
<rect x="26" y="160" width="204" height="16" rx="6" fill="#FFD23F"/>
<path d="M30 176 L226 176 Q226 222 128 222 Q30 222 30 176 Z" fill="url(#orange)"/>''',
 'MUSIC': f'''
<path d="M96 186 L96 52 L210 26 L210 160" fill="none" stroke-width="36"/>
<path d="M96 186 L96 52 L210 26 L210 160" fill="none" stroke="url(#purple)" stroke-width="20"/>
<path d="M96 70 L210 44" stroke="none"/>
<ellipse cx="70" cy="192" rx="40" ry="32" fill="url(#purple)"/>
<ellipse cx="184" cy="166" rx="40" ry="32" fill="url(#purple)"/>
<ellipse cx="58" cy="182" rx="12" ry="7" {HL}/>''',
 'SPORT': f'''
<circle cx="128" cy="128" r="104" fill="url(#grey)"/>
<path d="M128 84 L170 114 L154 162 L102 162 L86 114 Z" fill="#2D3444" stroke-width="5"/>
<g fill="none" stroke-width="6"><path d="M128 84 L128 26"/><path d="M170 114 L226 96"/><path d="M154 162 L190 214"/><path d="M102 162 L66 214"/><path d="M86 114 L30 96"/></g>
''',
 'COUNTRIES': f'''
<circle cx="128" cy="128" r="104" fill="url(#blue)"/>
<path d="M60 70 Q90 50 120 66 Q130 90 104 100 Q96 124 70 120 Q50 100 60 70 Z" fill="url(#green)" stroke-width="5"/>
<path d="M140 100 Q178 84 200 112 Q206 150 180 170 Q160 196 140 176 Q150 150 132 136 Q126 116 140 100 Z" fill="url(#green)" stroke-width="5"/>
<path d="M86 160 Q104 152 112 172 Q104 200 88 194 Z" fill="url(#green)" stroke-width="5"/>
<ellipse cx="84" cy="56" rx="24" ry="12" transform="rotate(-30 84 56)" {HL}/>''',
 'CINEMA': f'''
<rect x="30" y="98" width="196" height="126" rx="12" fill="url(#dark)"/>
<path d="M26 60 L214 30 L222 76 L34 106 Z" fill="url(#dark)"/>
<g stroke="none" fill="#fff"><path d="M58 56 L86 51 L70 98 L44 102 Z"/><path d="M114 47 L142 42 L126 89 L100 93 Z"/><path d="M170 38 L198 34 L182 80 L156 84 Z"/></g>
<g stroke="none" fill="#fff" opacity="0.9"><rect x="50" y="130" width="156" height="12" rx="6"/><rect x="50" y="166" width="110" height="12" rx="6"/></g>''',
 'ANIMALS': f'''
<ellipse cx="128" cy="168" rx="62" ry="54" fill="url(#orange)"/>
<ellipse cx="62" cy="108" rx="24" ry="30" fill="url(#orange)" transform="rotate(-20 62 108)"/>
<ellipse cx="102" cy="64" rx="24" ry="32" fill="url(#orange)" transform="rotate(-8 102 64)"/>
<ellipse cx="154" cy="64" rx="24" ry="32" fill="url(#orange)" transform="rotate(8 154 64)"/>
<ellipse cx="194" cy="108" rx="24" ry="30" fill="url(#orange)" transform="rotate(20 194 108)"/>''',
 'NATURE': f'''
<rect x="112" y="150" width="32" height="84" rx="6" fill="url(#wood)"/>
<circle cx="128" cy="96" r="70" fill="url(#green)"/>
<circle cx="72" cy="130" r="44" fill="url(#green)"/><circle cx="184" cy="130" r="44" fill="url(#green)"/>
<ellipse cx="100" cy="58" rx="24" ry="12" transform="rotate(-30 100 58)" {HL}/>''',
 'FRUIT & VEG': f'''
<path d="M128 70 Q70 40 42 90 Q20 150 66 206 Q96 238 128 220 Q160 238 190 206 Q236 150 214 90 Q186 40 128 70 Z" fill="url(#red)"/>
<path d="M128 72 Q132 40 150 22" fill="none" stroke-width="10"/>
<path d="M140 50 Q176 18 210 38 Q186 72 140 50 Z" fill="url(#green)" stroke-width="5"/>
<ellipse cx="76" cy="104" rx="20" ry="30" transform="rotate(20 76 104)" {HL}/>''',
 'JOBS': f'''
<rect x="86" y="34" width="84" height="44" rx="14" fill="none" stroke-width="26"/>
<rect x="86" y="34" width="84" height="44" rx="14" fill="none" stroke="url(#woodDark)" stroke-width="12"/>
<rect x="24" y="70" width="208" height="150" rx="20" fill="url(#wood)"/>
<rect x="24" y="118" width="208" height="30" fill="url(#woodDark)"/>
<rect x="110" y="110" width="36" height="44" rx="8" fill="url(#gold)"/>''',
 'BODY': f'''
<path d="M128 222 Q32 160 30 96 Q30 40 82 36 Q114 36 128 70 Q142 36 174 36 Q226 40 226 96 Q224 160 128 222 Z" fill="url(#pink)"/>
<ellipse cx="78" cy="80" rx="22" ry="14" transform="rotate(-30 78 80)" {HL}/>''',
 'CLOTHES': f'''
<path d="M86 30 Q128 66 170 30 L232 66 L206 124 L182 112 L182 226 L74 226 L74 112 L50 124 L24 66 Z" fill="url(#pink)"/>
<path d="M86 30 Q128 70 170 30" fill="none" stroke-width="8"/>
<path d="M74 160 L182 160" stroke="#fff" stroke-opacity="0.6" stroke-width="12"/>''',
 'WEATHER': f'''
<circle cx="88" cy="88" r="56" fill="url(#gold)"/>
<g stroke-width="10"><path d="M88 6 L88 22"/><path d="M8 88 L24 88"/><path d="M30 30 L42 42"/><path d="M146 30 L134 42"/></g>
<path d="M70 210 Q30 210 34 176 Q38 146 72 148 Q80 104 128 104 Q174 104 184 146 Q228 144 228 178 Q228 210 192 210 Z" fill="url(#grey)"/>''',
 'SPACE': f'''
<path d="M128 18 Q190 70 180 160 L76 160 Q66 70 128 18 Z" fill="url(#grey)"/>
<circle cx="128" cy="94" r="24" fill="url(#blue)" stroke-width="6"/>
<path d="M76 120 L36 178 L80 170 Z" fill="url(#red)"/><path d="M180 120 L220 178 L176 170 Z" fill="url(#red)"/>
<path d="M98 160 L158 160 L150 184 L106 184 Z" fill="url(#dark)"/>
<path d="M108 188 Q128 250 148 188 Z" fill="url(#orange)"/>''',
 'OCEAN': f'''
<path d="M20 140 Q60 90 104 128 Q144 162 180 116 Q210 82 236 110 L236 230 L20 230 Z" fill="url(#blue)"/>
<path d="M20 180 Q64 140 108 176 Q150 206 190 168 Q216 146 236 162" fill="none" stroke="#fff" stroke-width="10"/>
<path d="M120 80 Q150 40 196 60 Q176 80 196 100 Q150 120 120 80 Z" fill="url(#orange)" stroke-width="6"/>
<path d="M120 80 L94 60 L96 100 Z" fill="url(#orange)" stroke-width="6"/><circle cx="174" cy="74" r="6" fill="{OL}" stroke="none"/>''',
 'KITCHEN': f'''
<path d="M150 150 L236 236" stroke-width="34"/><path d="M150 150 L236 236" stroke="url(#woodDark)" stroke-width="20"/>
<circle cx="104" cy="104" r="86" fill="url(#dark)"/>
<circle cx="104" cy="104" r="62" fill="#3B4455" stroke-width="5"/>
<ellipse cx="104" cy="104" rx="34" ry="30" fill="#fff" stroke-width="5"/><circle cx="110" cy="100" r="16" fill="url(#gold)" stroke-width="4"/>''',
 'SCHOOL': f'''
<path d="M30 60 Q80 40 128 64 Q176 40 226 60 L226 210 Q176 190 128 212 Q80 190 30 210 Z" fill="url(#blue)"/>
<path d="M44 68 Q86 54 124 74 L124 196 Q86 178 44 192 Z" fill="url(#cream)" stroke-width="4"/>
<path d="M212 68 Q170 54 132 74 L132 196 Q170 178 212 192 Z" fill="url(#cream)" stroke-width="4"/>
<path d="M128 64 L128 212" stroke-width="6"/>''',
 'TRAVEL': f'''
<rect x="92" y="28" width="72" height="40" rx="12" fill="none" stroke-width="22"/>
<rect x="92" y="28" width="72" height="40" rx="12" fill="none" stroke="url(#grey)" stroke-width="8"/>
<rect x="36" y="60" width="184" height="160" rx="22" fill="url(#orange)"/>
<rect x="72" y="60" width="22" height="160" fill="url(#woodDark)"/><rect x="162" y="60" width="22" height="160" fill="url(#woodDark)"/>
<circle cx="70" cy="226" r="12" fill="url(#dark)"/><circle cx="186" cy="226" r="12" fill="url(#dark)"/>''',
}

for name, body in CAT.items():
    slug = 'cat_' + name.lower().replace(' & ', '_').replace(' ', '_')
    if body is None:
        body = open(os.path.join(OUT, 'icon_bulb.svg')).read().split('stroke-linecap="round">', 1)[1].rsplit('</g>', 1)[0]
    icon(slug.replace('icon_', ''), body)

if __name__ == '__main__':
    print('icons written')
