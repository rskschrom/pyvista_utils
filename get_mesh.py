import numpy as np
import pyvista as pv
from pyvista_util import create_cells

# read dipole positions
data = np.genfromtxt('geom_0046.txt', skip_header=3)
print(data.shape)

xd = data[:,0].astype(int)
yd = data[:,1].astype(int)
zd = data[:,2].astype(int)

# create uniform grid based on dipole locations
nx = np.max(xd)
ny = np.max(yd)
nz = np.max(zd)
values = np.zeros([nx,ny,nz])
values[xd-1,yd-1,zd-1] = 1
print(values[xd[-1]-1,yd[-1]-1,zd[-1]-1])

grid = pv.UniformGrid()
grid.dimensions = values.shape
grid.spacing = (1,1,1)
grid.point_data["values"] = values.flatten(order="F")

# get mesh from volume grid
mesh = grid.contour([1], method='marching_cubes')
smooth = mesh.smooth_taubin(n_iter=50, pass_band=0.1)

# save to file
smooth.save('aggregate.stl')

# plot
p = pv.Plotter()
p.enable_eye_dome_lighting()
p.add_mesh(smooth, color='c')
p.show()
