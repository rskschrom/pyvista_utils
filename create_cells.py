import numpy as np
import pyvista as pv
from netCDF4 import Dataset

# plot cell data
def cell_data_plot(ix, iy, iz, scalar):
    ncell = len(ix)

    # create cell and copy it ncell times
    ds = 0.1
    cell_template = np.array([[0.,0.,0.],
                             [ds,0.,0.],
                             [ds,ds,0.],
                             [0.,ds,0.],
                             [0.,0.,ds],
                             [ds,0.,ds],
                             [ds,ds,ds],
                             [0.,ds,ds]])
    cell_rep = np.tile(cell_template, (ncell, 1))

    # create xyz offset vectors
    xoffs = np.array([[1.,0.,0.]])
    yoffs = np.array([[0.,1.,0.]])
    zoffs = np.array([[0.,0.,1.]])

    # create position offset arrays at each cell point
    repxi = np.tile(xi, (8,1)).flatten(order='F').reshape((ncell*8,1))
    repyi = np.tile(yi, (8,1)).flatten(order='F').reshape((ncell*8,1))
    repzi = np.tile(zi, (8,1)).flatten(order='F').reshape((ncell*8,1))

    cell_points = cell_rep+repxi*ds*xoffs+repyi*ds*yoffs+repzi*ds*zoffs

    # create unstructured grid
    cells_hex = np.arange(ncell*8).reshape([ncell,8])
    grid = pv.UnstructuredGrid({pv.CellType.HEXAHEDRON: cells_hex}, cell_points)
    grid.cell_data['bin_tot'] = btot

    # plot
    p = pv.Plotter()
    p.add_mesh(grid, cmap='Spectral_r', opacity=0.3)
    p.show()
    return

# read file
ncfile = Dataset('lpvex_bin_ic.nc', 'r')
print(ncfile)
xi = ncfile.variables['xind'][:]
yi = ncfile.variables['yind'][:]
zi = ncfile.variables['zind'][:]
bd = ncfile.variables['bin_data'][:]
btot = np.sum(bd, axis=0)

cell_data_plot(xi, yi, zi, btot)
