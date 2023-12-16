import svgwrite
from svgwrite import cm, mm

dwg = svgwrite.Drawing('test.svg', profile='tiny')
#dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.text('Test1', insert=(0, 0.2), fill='red'))

part1 = dwg.add(dwg.g(id='part1', stroke='blue', fill='red'))
#part1.add(dwg.rect(insert=(5*cm, 5*cm), size=(45*mm, 45*mm), stroke_width=3))
#points = [(0,10),(10,10),(20,11),(0,10),(0,0)]
points = [(330,207),(388,205),(390,189),(414,189),(413,300),(390,300),(390,280),(325,280)]
part1.add(dwg.polygon(points))
#svgwrite.shapes.Polygon(points=[], **extra)

dwg.save()
