import svgwrite

version = '0.1'

inch = 25.4 * 3.7795 # pixels2inch
mat_thickness = 0.22
side_tab = 1.0
overhang = 0.25
top_tab = 0.5

# Placeholders. Implementatino needed
no_tab_threshold = 2.5
extra_top_tab_threshold = 24

box_height = float(input('box height: '))
box_width  = float(input('box width:  '))
box_depth  = float(input('box depth:  '))

#box_height = 10
#box_width  = 7
#box_depth  = 8


# box is always landscape-orientation: The width is always equal or larger than depth
if (box_width < box_depth):
    tmp = box_width
    box_width = box_depth
    box_depth = tmp


filename = '_'.join(['boxgen'+version, str(box_height)+'h', str(box_width)+'w', str(box_depth)+'d']) + '.svg'

dwg = svgwrite.Drawing(filename, profile='tiny')
top = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
front = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
side = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
sidecomplex = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
topcomplex = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))

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

# Side panel:
size_minus_overhang         = box_depth - overhang - overhang
size_minus_overhang_andtab = size_minus_overhang - top_tab
height_half_minus_tab       = (box_height - side_tab) / 2
points = [(0,0),(top_tab,0),(top_tab,mat_thickness),
          (size_minus_overhang_andtab, mat_thickness),(size_minus_overhang_andtab, 0),(size_minus_overhang,0),
          (size_minus_overhang,height_half_minus_tab),(size_minus_overhang-mat_thickness,height_half_minus_tab),
          (size_minus_overhang-mat_thickness,height_half_minus_tab+side_tab),(size_minus_overhang,height_half_minus_tab+side_tab),
          (size_minus_overhang,box_height),(size_minus_overhang-top_tab,box_height),
          (size_minus_overhang-top_tab,box_height-mat_thickness),
          (top_tab,box_height-mat_thickness),(top_tab,box_height),(0,box_height),(0,height_half_minus_tab+side_tab),(mat_thickness,height_half_minus_tab+side_tab),
          (mat_thickness,height_half_minus_tab),(0,height_half_minus_tab)]

tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate((box_width+1)*inch,0*inch)
tmp.scale(inch,inch)
side.add(tmp)

# Top panel:
points = [(0,0),(box_width,0),(box_width,box_depth),(0,box_depth)]
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate((box_width+box_depth+2)*inch,0*inch)
tmp.scale(inch,inch)
top.add(tmp)
# top panel - L's:
points = [(0,0),(mat_thickness+top_tab,0),(mat_thickness+top_tab,mat_thickness),(mat_thickness,mat_thickness),(mat_thickness,top_tab),(0,top_tab)]
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate(overhang*inch,overhang*inch)
tmp.translate((box_width+box_depth+2)*inch,0*inch)
tmp.scale(inch,inch)
top.add(tmp)
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate((box_width-overhang)*inch,overhang*inch)
tmp.translate((box_width+box_depth+2)*inch,0*inch)
tmp.scale(-inch,inch)
top.add(tmp)
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate((box_width-overhang)*inch,(box_depth-overhang)*inch)
tmp.translate((box_width+box_depth+2)*inch,0*inch)
tmp.scale(-inch,-inch)
top.add(tmp)
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate(overhang*inch,(box_depth-overhang)*inch)
tmp.translate((box_width+box_depth+2)*inch,0*inch)
tmp.scale(inch,-inch)
top.add(tmp)

# 4-sides complex:
part1size1 = box_width - overhang - overhang - mat_thickness - mat_thickness
part1size2 = part1size1 - top_tab
part1top = [(0,0),(top_tab,0),(top_tab,mat_thickness),
          (part1size2, mat_thickness),(part1size2, 0),(part1size1,0)]

part2size1 = box_depth - overhang - overhang
part2size2 = part2size1 - top_tab
part2top = [(0,0),(top_tab,0),(top_tab,mat_thickness),
          (part2size2, mat_thickness),(part2size2, 0),(part2size1,0)]


part2_translated = [(x[0]+part1size1, x[1]) for x in part2top]
part12 = part1top + part2_translated
part12_doubled = part12 + [(x[0]+part1size1+part2size1, x[1]) for x in part12]
part12_doubled_updown = [(x[0], box_height-x[1]) for x in part12_doubled]

part3 = [ (0,0), (0,height_half_minus_tab), (-mat_thickness,height_half_minus_tab),
          (-mat_thickness,height_half_minus_tab+side_tab),(0,height_half_minus_tab+side_tab),(0,box_height)]
part4 = [(part1size1-x[0], x[1]) for x in part3]

part3_shifted = [(part1size1+part2size1+x[0], x[1]) for x in part3]
part4_shifted = [(part1size1+part2size1+x[0], x[1]) for x in part4]
part3_shifted2 = [(part1size1+part2size1+x[0], x[1]) for x in part3_shifted]

for points in (part12_doubled_updown,part12_doubled, part3, part4, part3_shifted,part4_shifted,part3_shifted2):
    tmp = dwg.polyline(points, stroke_width=0.1)
    tmp.translate(0*inch,(box_height+1)*inch)
    tmp.scale(inch,inch)
    sidecomplex.add(tmp)

#top-complex:
position_top_complex_x = 0*inch
position_top_complex_y = (box_height+1)*2*inch
points = [(0,0),(box_width,0),(box_width,2*box_depth),(0,2*box_depth)]
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate(position_top_complex_x, position_top_complex_y)
tmp.scale(inch,inch)
topcomplex.add(tmp)
points = [(0,box_depth),(box_width,box_depth)]
tmp = dwg.polygon(points, stroke_width=0.1)
tmp.translate(position_top_complex_x, position_top_complex_y)
tmp.scale(inch,inch)
topcomplex.add(tmp)


for yoffset in (0, box_depth):
    # top panel - L's:
    points = [(0,0),(mat_thickness+top_tab,0),(mat_thickness+top_tab,mat_thickness),(mat_thickness,mat_thickness),(mat_thickness,top_tab),(0,top_tab)]
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(overhang*inch,(overhang+yoffset)*inch)
    tmp.translate(position_top_complex_x, position_top_complex_y)
    tmp.scale(inch,inch)
    topcomplex.add(tmp)
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate((box_width-overhang)*inch,(overhang+yoffset)*inch)
    tmp.translate(position_top_complex_x, position_top_complex_y)
    tmp.scale(-inch,inch)
    topcomplex.add(tmp)
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate((box_width-overhang)*inch,(box_depth-overhang+yoffset)*inch)
    tmp.translate(position_top_complex_x, position_top_complex_y)
    tmp.scale(-inch,-inch)
    topcomplex.add(tmp)
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(overhang*inch,(box_depth-overhang+yoffset)*inch)
    tmp.translate(position_top_complex_x, position_top_complex_y)
    tmp.scale(inch,-inch)
    topcomplex.add(tmp)

dwg.save()
print ('saved: ', filename)
