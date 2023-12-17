import svgwrite
from svgwrite import cm, mm #, inch

inch = 25.4 * 3.7795 # pixels2inch
mat_thickness = 0.22
side_tab = 1.0
overhang = 0.125
top_tab = 0.5
no_tab_threshold = 2.5

# box is always landscape-orientation

box_height = 10
box_width = 8
box_depth = 8

dwg = svgwrite.Drawing('test.svg', profile='tiny')
#dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.text('Test1', insert=(0, 0.2), fill='red'))

top = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
front = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
side = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
#part1.add(dwg.rect(insert=(5*cm, 5*cm), size=(45*mm, 45*mm), stroke_width=3))
#points = [(330,207),(388,205),(390,189),(414,189),(413,300),(390,300),(390,280),(325,280)]
#points = [(0*inch,0*inch),(box_width*inch,0*inch),(box_width*inch,box_depth*inch),(0*inch,box_depth*inch)]
points = [(0,0),(box_width,0),(box_width,box_depth),(0,box_depth)]

# scale does not affect translation:
tmp = dwg.polygon(points)
tmp.translate(7*inch,7*inch)
tmp.scale(inch,inch)
#top.add(tmp)

# To add another, create a new polygon
tmp = dwg.polygon(points)
tmp.scale(inch,inch)
#top.add(tmp)

# Front panel:
size_minus_overhang         = box_width - overhang - overhang - mat_thickness - mat_thickness
size_minus_overhang_andtab = size_minus_overhang - top_tab
height_half_minus_tab       = (box_height - side_tab) / 2
points = [(0,0),(top_tab,0),(top_tab,mat_thickness),
          (size_minus_overhang_andtab, mat_thickness),(size_minus_overhang_andtab, 0),(size_minus_overhang,0),
          (size_minus_overhang,height_half_minus_tab),(size_minus_overhang+mat_thickness,height_half_minus_tab),
          (size_minus_overhang+mat_thickness,height_half_minus_tab+side_tab),(size_minus_overhang,height_half_minus_tab+side_tab),
          (size_minus_overhang,box_height),(size_minus_overhang-top_tab,box_height),
          (size_minus_overhang-top_tab,box_height-mat_thickness),
          (top_tab,box_height-mat_thickness),(top_tab,box_height),(0,box_height),(0,height_half_minus_tab+side_tab),(-mat_thickness,height_half_minus_tab+side_tab),
          (-mat_thickness,height_half_minus_tab),(0,height_half_minus_tab)]

tmp = dwg.polygon(points, stroke_width=0.1)
tmp.scale(inch,inch)
front.add(tmp)


dwg.save()
