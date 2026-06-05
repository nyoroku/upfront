import base64
import os

jpg_path = 'c:/Users/Administrator/PycharmProjects/worklane/static/images/worklanelogo.jpg'
svg_out = 'c:/Users/Administrator/PycharmProjects/worklane/static/images/worklane_logo.svg'

with open(jpg_path, 'rb') as f:
    img_data = f.read()
    b64_str = base64.b64encode(img_data).decode('utf-8')

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500">
  <image href="data:image/jpeg;base64,{b64_str}" width="100%" height="100%" preserveAspectRatio="xMidYMid meet"/>
</svg>"""

with open(svg_out, 'w') as f:
    f.write(svg_content)

print(f"Created SVG at {svg_out}")
