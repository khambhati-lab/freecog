import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def generate_fig(SUBJECT_ID, GEOM, DF_ELECTRODES, node_radius=5):
    # Create blank axis
    axis = dict(showbackground=False,
                showline=False,
                zeroline=False,
                showgrid=False,
                showticklabels=False,
                title='')

    # Create Layout
    layout = go.Layout(title=SUBJECT_ID,
                width=1280,
                height=720,
                showlegend=False,
                scene=dict(xaxis=dict(axis),
                        yaxis=dict(axis),
                        zaxis=dict(axis),
                        ),
                margin=dict(t=50),
                hovermode='closest')

    # Create a figure
    fig = go.Figure(layout=layout)    
    
    # Create mesh
    for ii, anat in enumerate(GEOM):
        for hemi in GEOM[anat]:
            fig.add_trace(go.Mesh3d(
                            name=f"{hemi}-{GEOM[anat][hemi]['text']}",
                
                            # x, y, and z give the positions of the vertices
                            x=GEOM[anat][hemi]['vert'][:,0],
                            y=GEOM[anat][hemi]['vert'][:,1],
                            z=GEOM[anat][hemi]['vert'][:,2],
    
                            # i, j and k give the vertex indices of the triangles
                            i=GEOM[anat][hemi]['tri'][:,0],
                            j=GEOM[anat][hemi]['tri'][:,1],
                            k=GEOM[anat][hemi]['tri'][:,2],  
    
                            # Intensity of each vertex, which will be interpolated and color-coded
                            intensity = np.linspace(0, 1, 32, endpoint=True),
                            intensitymode='cell',
                            colorscale=[[0, GEOM[anat][hemi]['color']],
                                        [1, GEOM[anat][hemi]['color']]],        
                            opacity=GEOM[anat][hemi]['opacity'],
                            showscale=False,
                            showlegend=True,
                            text=GEOM[anat][hemi]['text'],
                            hoverinfo='text',
                        ))

    # Trace the nodes        
    fig.add_trace(go.Scatter3d(x=DF_ELECTRODES['x'],
                               y=DF_ELECTRODES['y'],
                               z=DF_ELECTRODES['z'],
                            mode='markers',
                            marker=dict(symbol='circle',
                                        size=DF_ELECTRODES['radius'],
                                        color=DF_ELECTRODES['color'],  # SPECIFY COLOR RGB FOR EACH CONTACT,
                                        line_width=0,
                                        line=None),
                            text=[('<br>').join(['{}: {}'.format(key, row[1].to_dict()[key])
                                                 for key in row[1][['Contact']].to_dict()])
                                  for row in DF_ELECTRODES.iterrows()],
                            showlegend=False,
                            hoverinfo='text'))

    # Remove legend
    fig.update_layout(showlegend = True, legend_title_text='Anatomical Meshes: Click to Toggle On/Off')

    # Remove tick labels
    fig.update_xaxes(showticklabels = False)
    fig.update_yaxes(showticklabels = False)

    return fig











