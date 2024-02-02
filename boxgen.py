import svgwrite

version = '0.2'
inch = 25.4 * 3.7795 # pixels2inch

#### PARAM BLOCK ######################
mat_thickness = 0.22
side_tab = 1.0
overhang = 0.25
top_tab = 0.5
centertop_tab = 1.0
tightness = 0.01 # Makes the holes at the top and bottom tighter
short_sidetab_threshold = 3.0
no_sidetab_threshold = 0.0
extra_top_tab_threshold = 24
draw_individual = True
draw_fourside = True
draw_dualtop1 = True
draw_dualtop2 = True
#### PARAM BLOCK - END  ##############

box_height = float(input('box height: '))
box_width  = float(input('box width:  '))
box_depth  = float(input('box depth:  '))

#box_height = 10
#box_width  = 25
#box_depth  = 28

# box is always landscape-orientation: The width is always equal or larger than depth
if (box_width < box_depth):
    tmp = box_width
    box_width = box_depth
    box_depth = tmp

# apply a short side-tab:
if (box_height <= short_sidetab_threshold):
    side_tab = side_tab / 2

filename = '_'.join(['boxgen'+version, str(box_height)+'h', str(box_width)+'w', str(box_depth)+'d']) + '.svg'

dwg = svgwrite.Drawing(filename, profile='tiny')
top = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
front = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
side = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
sidecomplex = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
topcomplex = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
topcomplex2 = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))

# Commonly used metric:
height_half_minus_tab       = (box_height - side_tab) / 2

def top_panel_add_ls(panel, posx, posy):
    points = [(0,0),(mat_thickness+top_tab-tightness,0),(mat_thickness+top_tab-tightness,mat_thickness-tightness),(mat_thickness-tightness,mat_thickness-tightness),(mat_thickness-tightness,top_tab-tightness),(0,top_tab-tightness)]
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(overhang*inch,overhang*inch)
    tmp.translate(posx,posy)
    tmp.scale(inch,inch)
    panel.add(tmp)
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate((box_width-overhang)*inch,overhang*inch)
    tmp.translate(posx,posy)
    tmp.scale(-inch,inch)
    panel.add(tmp)
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate((box_width-overhang)*inch,(box_depth-overhang)*inch)
    tmp.translate(posx,posy)
    tmp.scale(-inch,-inch)
    panel.add(tmp)
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(overhang*inch,(box_depth-overhang)*inch)
    tmp.translate(posx,posy)
    tmp.scale(inch,-inch)
    panel.add(tmp)
    # I's if present:
    if (box_width >= extra_top_tab_threshold):
        for (yy,sy) in ((overhang,1), (box_depth-overhang,-1)):
            points = [(0,0),(centertop_tab-tightness,0),(centertop_tab-tightness,mat_thickness-tightness),(0,mat_thickness-tightness)]
            tmp = dwg.polygon(points, stroke_width=0.1)
            tmp.translate((box_width-centertop_tab)/2*inch,(yy)*inch)
            tmp.translate(posx,posy)
            tmp.scale(inch,inch*sy)
            panel.add(tmp)
    if (box_depth >= extra_top_tab_threshold):
        for (xx,sx) in ((overhang,1), (box_width-overhang,-1)):
            points = [(0,0),(mat_thickness-tightness,0),(mat_thickness-tightness,centertop_tab-tightness),(0,centertop_tab-tightness)]
            tmp = dwg.polygon(points, stroke_width=0.1)
            tmp.translate(xx*inch,(((box_depth-centertop_tab)/2))*inch)
            tmp.translate(posx,posy)
            tmp.scale(inch*sx,inch)
            panel.add(tmp)

# Top panel:
if (draw_individual):
    top_panel_posx = -(max(box_width,box_depth)+1)*inch
    top_panel_posy = 0*inch
    points = [(0,0),(box_width,0),(box_width,box_depth),(0,box_depth)]
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(top_panel_posx,top_panel_posy)
    tmp.scale(inch,inch)
    top.add(tmp)
    top_panel_add_ls(top, top_panel_posx, top_panel_posy)

# 4-sides complex:
part1size1 = box_width - overhang - overhang - mat_thickness - mat_thickness
part1size2 = part1size1 - top_tab
part1size3 = (part1size1 - centertop_tab) / 2

if (box_width < extra_top_tab_threshold):
    part1top = [(0,0),(top_tab,0),(top_tab,mat_thickness),
            (part1size2, mat_thickness),(part1size2, 0),(part1size1,0)]
else:
    part1top = [(0,0),(top_tab,0),(top_tab,mat_thickness),
                (part1size3, mat_thickness),(part1size3, 0),(part1size3 + centertop_tab, 0), (part1size3 + centertop_tab, mat_thickness),
                (part1size2, mat_thickness),(part1size2, 0),(part1size1,0)]


part2size1 = box_depth - overhang - overhang
part2size2 = part2size1 - top_tab
part2size3 = (part2size1 - centertop_tab) / 2
if (box_depth < extra_top_tab_threshold):
    part2top = [(0,0),(top_tab,0),(top_tab,mat_thickness),
            (part2size2, mat_thickness),(part2size2, 0),(part2size1,0)]
else:
    part2top = [(0,0),(top_tab,0),(top_tab,mat_thickness),
                    (part2size3, mat_thickness),(part2size3, 0),(part2size3 + centertop_tab, 0), (part2size3 + centertop_tab, mat_thickness),
                    (part2size2, mat_thickness),(part2size2, 0),(part2size1,0)]

part2_translated = [(x[0]+part1size1, x[1]) for x in part2top]
part12 = part1top + part2_translated
part12_doubled = part12 + [(x[0]+part1size1+part2size1, x[1]) for x in part12]
part12_doubled_updown = [(x[0], box_height-x[1]) for x in part12_doubled]

if (box_height > no_sidetab_threshold):
    part3 = [ (0,0), (0,height_half_minus_tab), (-mat_thickness,height_half_minus_tab),
            (-mat_thickness,height_half_minus_tab+side_tab),(0,height_half_minus_tab+side_tab),(0,box_height)]
else:
    part3 = [ (0,0), (0,box_height)]

part4 = [(part1size1-x[0], x[1]) for x in part3]

part3_shifted = [(part1size1+part2size1+x[0], x[1]) for x in part3]
part4_shifted = [(part1size1+part2size1+x[0], x[1]) for x in part4]
part3_shifted2 = [(part1size1+part2size1+x[0], x[1]) for x in part3_shifted]

if (draw_fourside):
    for points in (part12_doubled_updown,part12_doubled, part3, part4, part3_shifted,part4_shifted,part3_shifted2):
        tmp = dwg.polyline(points, stroke_width=0.1)
        tmp.translate(0*inch,(box_height+1)*inch)
        tmp.scale(inch,inch)
        sidecomplex.add(tmp)

# Front panel:
if (draw_individual):
    part1bottom = [(x[0], box_height-x[1]) for x in part1top]
    points = part1top + part4 + part1bottom[::-1] + part3[::-1]

    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.scale(inch,inch)
    front.add(tmp)

    # Side panel:
    part2bottom = [(x[0], box_height-x[1]) for x in part2top]
    part3_negative = [(-x[0], x[1]) for x in part3]
    points = part2top + [(part2size1+x[0], x[1]) for x in part3] + part2bottom[::-1] + part3_negative[::-1]

    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate((box_width+1)*inch,0*inch)
    tmp.scale(inch,inch)
    side.add(tmp)

#top-complex:
if (draw_dualtop1):
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
    for yoffset in (0, box_depth*inch):
        top_panel_add_ls(topcomplex, position_top_complex_x, position_top_complex_y+yoffset)

#top-complex-2:
if (draw_dualtop2):
    position_top_complex_x = (max(box_width,box_depth)+1)*inch
    position_top_complex_y = (box_height+1)*2*inch
    points = [(0,0),(box_width*2,0),(box_width*2,box_depth),(0,box_depth)]
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(position_top_complex_x, position_top_complex_y)
    tmp.scale(inch,inch)
    topcomplex2.add(tmp)
    points = [(box_width,0),(box_width,box_depth)]
    tmp = dwg.polygon(points, stroke_width=0.1)
    tmp.translate(position_top_complex_x, position_top_complex_y)
    tmp.scale(inch,inch)
    topcomplex2.add(tmp)
    for xoffset in (0, box_width*inch):
        top_panel_add_ls(topcomplex2, position_top_complex_x+xoffset, position_top_complex_y)

dwg.save()
print ('saved: ', filename)
