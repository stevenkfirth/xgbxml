# -*- coding: utf-8 -*-

from .geometry_functions import polygon_triangulate_3d

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


def get_matplotlib_fig_ax(nD):
    """
    """
    if nD==2:
        fig, ax = plt.subplots()
        
    elif nD==3:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_zlabel('z-coordinate')
    else:
        raise Exception
        
    ax.set_xlabel('x-coordinate')
    ax.set_ylabel('y-coordinate')
    return fig,ax


def render_polygon_3d(polygon,
                      polygon_triangles=None,
                      ax=None, 
                      set_lims=True, 
                      outline_kwargs=None,
                      surface_kwargs=None):
    """Plots the polygon on the supplied axes.
        
    :param ax: An 2D or 3D Axes instance.
    :type ax:  matplotlib.axes._subplots.AxesSubplot, matplotlib.axes._subplots.Axes3DSubplot
    :param kwargs: keyword arguments to be passed to the Axes.plot call.
               
    :returns: The matplotlib axes.
    :rtype: matplotlib.axes._subplots.AxesSubplot or 
    matplotlib.axes._subplots.Axes3DSubplot

    """
    if ax is None:
        fig,ax=get_matplotlib_fig_ax(3)

    if outline_kwargs is None:
        outline_kwargs={}
    
    if surface_kwargs is None:
        surface_kwargs={}
        
    surface_kwargs['color']=surface_kwargs.get('color','tab:blue')
    surface_kwargs['alpha']=surface_kwargs.get('alpha',0.2)
    surface_kwargs['linewidth']=surface_kwargs.get('linewidth',0)
    
    shell, holes=polygon
    
    if polygon_triangles is None:
        polygon_triangles=polygon_triangulate_3d(shell,holes)
    
    verts=[tri[:-1] for tri in polygon_triangles]
    pc=Poly3DCollection(verts,**surface_kwargs)
    ax.add_collection3d(pc)
            
    outline_kwargs['color']=outline_kwargs.get('color','tab:blue')
    
    ax.plot(*zip(*shell), 
            **outline_kwargs)
    
    if set_lims:
        ax=set_ax_lims(ax)    

    return ax



def set_ax_lims(ax):
    """
    """
    xs, ys, zs = [], [], []
    for line in ax.get_lines():
        xs1, ys1, zs1 = line.get_data_3d()
        xs.extend(xs1)
        ys.extend(ys1)
        zs.extend(zs1)
        
    if len(xs)==0:
        return ax
        
    minx,maxx,miny,maxy,minz,maxz=min(xs),max(xs),min(ys),max(ys),min(zs),max(zs)
    maxrange=max([maxx-minx,maxy-miny,maxz-minz])
    xc,yc,zc=(maxx+minx)/2,(maxy+miny)/2,(maxz+minz)/2  # center or average
    
    x0,x1=xc-maxrange/2,xc+maxrange/2
    y0,y1=yc-maxrange/2,yc+maxrange/2
    z0,z1=zc-maxrange/2,zc+maxrange/2
    
    #if minx != maxx: 
    ax.set_xlim(x0,x1)
    #if miny != maxy: 
    ax.set_ylim(y0,y1)
    #if minz != maxz: 
    ax.set_zlim(z0,z1)
    
    return ax
    
