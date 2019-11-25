####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################

# Blender imports
import bpy
from bpy.props import EnumProperty
from bpy.props import IntProperty
from bpy.props import FloatProperty
from bpy.props import FloatVectorProperty
from bpy.props import BoolProperty

# Internal imports
import nmv
import nmv.consts
import nmv.enums
import nmv.utilities


# Meshing technique
bpy.types.Scene.NMV_MeshingTechnique = EnumProperty(
    items=[(nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT,
            'Piecewise Watertight',
            'This approach (Abdellah et al., 2017) creates a piecewise watertight mesh that is '
            'composed of multiple mesh objects, where each object is a watertight component. '
            'This method is used to reconstruct high fidelity volumes from the generated meshes'),
           (nmv.enums.Meshing.Technique.SKINNING,
            'Skinning',
            'Skinning (Abdellah et al., 2019) uses the skin modifier to reconstruct the branches. '
            'This approach is guaranteed to reconstruct a nice looking branching compared to the '
            'other methods and also guarantees the fidelity of the mesh, but it does not '
            'guarantee watertightness. This technique is used when you need meshes for '
            'visualization with transparency'),
           (nmv.enums.Meshing.Technique.UNION,
            'Union',
            'This method uses the union boolean operator to join the different branches together '
            'in a single mesh. It is not guaranteed to generate a watertight or even a valid '
            'mesh, although it works in 90% of the cases'),
           (nmv.enums.Meshing.Technique.META_OBJECTS,
            'MetaBalls',
            'Creates watertight mesh models using MetaBalls. This approach is extremely slow if '
            'the axons are included in the meshing process, so it is always recommended to use '
            'first order branching for the axons when using this technique')],
    name='Method',
    description='The technique that will be used to create the mesh, by default the '
                'Piecewise Watertight one since it is the fastest one.',
    default=nmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT)


# Build soma
bpy.types.Scene.NMV_MeshingPiecewiseFilling = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Representation.META_BALLS,
            'Connected Sections',
            'The stems are created using a series of connected sections starting from the root '
            'section to the leaves. The sections are overlapping at the branching points'),
           (nmv.enums.Soma.Representation.SOFT_BODY,
            'Disconnected Sections',
            'The stems area created using a series of disconnected sections, where each section '
            'is created as an individual watertight mesh. Additionally, sphers are added at the branching points.')],
    name='',
    default=nmv.enums.Soma.Representation.SOFT_BODY)

bpy.types.Scene.NMV_MeshingPiecewiseComponents = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.PiecewiseComponents.PATHS,
            'Paths',
            ''),
           (nmv.enums.Meshing.PiecewiseComponents.SECTIONS,
            'Sections',
            '')],
    name='Mesh Components',
    default=nmv.enums.Meshing.PiecewiseComponents.PATHS)

# Build soma
bpy.types.Scene.NMV_MeshingPiecewiseSoma = bpy.props.EnumProperty(
    items=[(nmv.enums.Soma.Representation.META_BALLS,
            'MetaBalls',
            'Reconstruct a rough shape of the soma using MetaBalls. '
            'This approach is real-time and can reconstruct good shapes for the somata, but '
            'more accurate profiles could be reconstructed with the Soft Body option'),
           (nmv.enums.Soma.Representation.SOFT_BODY,
            'Soft Body',
            'Reconstruct a 3D profile of the soma using Soft Body physics.'
            'This method takes few seconds to reconstruct a soma mesh')],
    name='Soma',
    default=nmv.enums.Soma.Representation.SOFT_BODY)


# Is the soma connected to the first order branches or not !
bpy.types.Scene.NMV_SomaArborsConnection = EnumProperty(
    items=[(nmv.enums.Meshing.SomaConnection.CONNECTED,
            'Connected',
            'Connect the soma mesh to the arbors to make a nice mesh that can be used for any'
            'type of visualization that involves transparency.'),
           (nmv.enums.Meshing.SomaConnection.DISCONNECTED,
            'Disconnected',
            'Create the soma as a separate mesh and do not connect it to the arbors. This '
            'option is used to guarantee surface smoothing when a volume is reconstructed '
            'from the resulting mesh, but cannot be used for surface transparency rendering.')],
    name='Soma Connection',
    default=nmv.enums.Meshing.SomaConnection.DISCONNECTED)

# The skeleton of the union-based meshing algorithm
bpy.types.Scene.NMV_UnionMethodSkeleton = EnumProperty(
    items=[(nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON,
            'Quad',
            'Use a quad skeleton for the union meshing algorithm'),
           (nmv.enums.Meshing.UnionMeshing.CIRCULAR_SKELETON,
            'Circle',
            'Use a circular skeleton for the union meshing algorithm')],
    name='Skeleton',
    default=nmv.enums.Meshing.UnionMeshing.QUAD_SKELETON)

# Edges, hard or smooth
bpy.types.Scene.NMV_MeshSmoothing = EnumProperty(
    items=[(nmv.enums.Meshing.Edges.HARD,
            'Sharp',
            'Make the edges between the segments sharp and hard'),
           (nmv.enums.Meshing.Edges.SMOOTH,
            'Curvy',
            'Make the edges between the segments soft and curvy')],
    name='Edges',
    default=nmv.enums.Meshing.Edges.HARD)

# Branching, is it based on angles or radii
bpy.types.Scene.NMV_MeshBranching = EnumProperty(
    items=[(nmv.enums.Meshing.Branching.ANGLES,
            'Angles',
            'Make the branching based on the angles at branching points'),
           (nmv.enums.Meshing.Branching.RADII,
            'Radii',
            'Make the branching based on the radii of the children at the branching points')],
    name='Branching Method',
    default=nmv.enums.Meshing.Branching.ANGLES)

# Are the mesh objects connected or disconnected.
bpy.types.Scene.NMV_MeshObjectsConnection = EnumProperty(
    items=[(nmv.enums.Meshing.ObjectsConnection.CONNECTED,
            'Connected',
            'Connect all the objects of the mesh into one piece'),
           (nmv.enums.Meshing.ObjectsConnection.DISCONNECTED,
            'Disconnected',
            'Keep the different mesh objects of the neuron into separate pieces')],
    name='Mesh Objects',
    default=nmv.enums.Meshing.ObjectsConnection.DISCONNECTED)

# Is the output model for reality or beauty
bpy.types.Scene.NMV_SurfaceRoughness = EnumProperty(
    items=[(nmv.enums.Meshing.Surface.ROUGH,
            'Rough',
            'Create a mesh that looks like a real neuron reconstructed from microscope'),
           (nmv.enums.Meshing.Surface.SMOOTH,
            'Smooth',
            'Create a mesh that has smooth surface for visualization')],
    name='Model',
    default=nmv.enums.Meshing.Surface.SMOOTH)

# Spine sources can be random or from a BBP circuit
bpy.types.Scene.NMV_SpinesSourceCircuit = EnumProperty(
    items=[(nmv.enums.Meshing.Spines.Source.IGNORE,
            'Ignore',
            'Ignore creating the spines'),
           (nmv.enums.Meshing.Spines.Source.RANDOM,
            'Random',
            'The spines are generated randomly'),
           (nmv.enums.Meshing.Spines.Source.CIRCUIT,
            'Circuit',
            'The spines are generated following a BBP circuit'),],
    name='Spines Source',
    default=nmv.enums.Meshing.Spines.Source.IGNORE)

# Spine sources are only random
bpy.types.Scene.NMV_SpinesSourceRandom = EnumProperty(
    items=[(nmv.enums.Meshing.Spines.Source.IGNORE,
            'Ignore',
            'Ignore creating the spines'),
           (nmv.enums.Meshing.Spines.Source.RANDOM,
            'Random',
            'The spines are generated randomly')],
    name='Spines Source',
    default=nmv.enums.Meshing.Spines.Source.IGNORE)

# Spine meshes quality
bpy.types.Scene.NMV_SpineMeshQuality = EnumProperty(
    items=[(nmv.enums.Meshing.Spines.Quality.LQ,
            'Low',
            'Load low quality meshes'),
           (nmv.enums.Meshing.Spines.Quality.HQ,
            'High',
            'Load high quality meshes')],
    name='Spines Quality',
    default=nmv.enums.Meshing.Spines.Quality.LQ)

# Nucleus
bpy.types.Scene.NMV_Nucleus = EnumProperty(
    items=[(nmv.enums.Meshing.Nucleus.IGNORE,
            'Ignore',
            'The nucleus is ignored'),
           (nmv.enums.Meshing.Nucleus.INTEGRATED,
            'Integrated',
            'The nucleus is integrated')],
    name='Nucleus',
    default=nmv.enums.Meshing.Nucleus.IGNORE)

# Nucleus mesh quality
bpy.types.Scene.NMV_NucleusMeshQuality = EnumProperty(
    items=[(nmv.enums.Meshing.Nucleus.Quality.LQ,
            'Low',
            'Low quality nucleus mesh'),
           (nmv.enums.Meshing.Nucleus.Quality.HQ,
            'High',
            'High quality nucleus mesh')],
    name='Nucleus Mesh Quality',
    default=nmv.enums.Meshing.Nucleus.Quality.LQ)

# Fix artifacts flag
bpy.types.Scene.NMV_FixMorphologyArtifacts = BoolProperty(
    name='Fix Morphology Artifacts',
    description='Fixes the morphology artifacts during the mesh reconstruction process',
    default=True)

# Mesh tessellation flag
bpy.types.Scene.NMV_TessellateMesh = BoolProperty(
    name='Tessellation',
    description='Tessellate the reconstructed mesh to reduce the geometry complexity',
    default=False)

# Mesh tessellation level
bpy.types.Scene.NMV_MeshTessellationLevel = FloatProperty(
    name='Factor',
    description='Mesh tessellation level (between 0.1 and 1.0)',
    default=1.0, min=0.1, max=1.0)

# Random spines percentage
bpy.types.Scene.NMV_RandomSpinesPercentage = FloatProperty(
    name='Percentage',
    description='The percentage of the random spines along the dendrites (1 - 100)',
    default=50, min=1.0, max=100.0)

bpy.types.Scene.NMV_MeshMaterial = EnumProperty(
    items=nmv.enums.Shading.MATERIAL_ITEMS,
    name="Material",
    default=nmv.enums.Shading.LAMBERT_WARD)

# Use single color for the all the objects in the mesh
bpy.types.Scene.NMV_MeshHomogeneousColor = BoolProperty(
    name="Homogeneous Color",
    description="Use a single color for rendering all the objects of the mesh",
    default=False)

# A homogeneous color for all the objects of the mesh (membrane and spines)
bpy.types.Scene.NMV_NeuronMeshColor = FloatVectorProperty(
    name="Membrane Color", subtype='COLOR',
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description="The homogeneous color of the reconstructed mesh membrane")

# The color of the reconstructed soma mesh
bpy.types.Scene.NMV_SomaMeshColor = FloatVectorProperty(
    name="Soma Color", subtype='COLOR',
    default=nmv.enums.Color.SOMA, min=0.0, max=1.0,
    description="The color of the reconstructed soma mesh")

# The color of the reconstructed axon mesh
bpy.types.Scene.NMV_AxonMeshColor = FloatVectorProperty(
    name="Axon Color", subtype='COLOR',
    default=nmv.enums.Color.AXONS, min=0.0, max=1.0,
    description="The color of the reconstructed axon mesh")

# The color of the reconstructed basal dendrites meshes
bpy.types.Scene.NMV_BasalDendritesMeshColor = FloatVectorProperty(
    name="Basal Dendrites Color", subtype='COLOR',
    default=nmv.enums.Color.BASAL_DENDRITES, min=0.0, max=1.0,
    description="The color of the reconstructed basal dendrites")

# The color of the reconstructed apical dendrite meshes
bpy.types.Scene.NMV_ApicalDendriteMeshColor = FloatVectorProperty(
    name="Apical Dendrite Color", subtype='COLOR',
    default=nmv.enums.Color.APICAL_DENDRITES, min=0.0, max=1.0,
    description="The color of the reconstructed apical dendrite")

# The color of the spines meshes
bpy.types.Scene.NMV_SpinesMeshColor = FloatVectorProperty(
    name="Spines Color", subtype='COLOR',
    default=nmv.enums.Color.SPINES, min=0.0, max=1.0,
    description="The color of the spines")

# The color of the nucleus mesh
bpy.types.Scene.NMV_NucleusMeshColor = FloatVectorProperty(
    name="Nucleus Color", subtype='COLOR',
    default=nmv.enums.Color.NUCLEI, min=0.0, max=1.0,
    description="The color of the nucleus")

# Rendering resolution
bpy.types.Scene.NMV_MeshRenderingResolution = EnumProperty(
    items=[(nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION,
            'Fixed',
            'Renders an image of the mesh at a specific resolution'),
           (nmv.enums.Meshing.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'Renders an image of the mesh at factor of the exact scale in (um)')],
    name='Type',
    default=nmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION)

# Rendering view
bpy.types.Scene.NMV_MeshRenderingView = EnumProperty(
    items=[(nmv.enums.Meshing.Rendering.View.WIDE_SHOT_VIEW,
            'Wide Shot',
            'Renders an image of the full view'),
           (nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW,
            'Mid Shot',
            'Renders an image of the reconstructed arbors only'),
           (nmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW,
            'Close Up',
            'Renders a close up image the focuses on the soma')],
    name='View', default=nmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW)

# Keep cameras
bpy.types.Scene.NMV_KeepMeshCameras = BoolProperty(
    name="Keep Cameras & Lights in Scene",
    description="Keep the cameras in the scene to be used later if this file is saved",
    default=False)

# Image resolution
bpy.types.Scene.NMV_MeshFrameResolution = IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the mesh',
    default=512, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.NMV_MeshFrameScaleFactor = FloatProperty(
    name="Scale", default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a mesh to scale")

# Mesh rendering close up size
bpy.types.Scene.NMV_MeshCloseUpSize = FloatProperty(
    name='Size',
    description='The size of the view that will be rendered in microns',
    default=20, min=5, max=100,)

# Soma rendering progress bar
bpy.types.Scene.NMV_NeuronMeshRenderingProgress = IntProperty(
    name="Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Individual components export flag
bpy.types.Scene.NMV_ExportIndividuals = BoolProperty(
    name='Export Components',
    description='Export each component of the neuron as a separate mesh. This feature is '
                'important to label reconstructions with machine learning applications',
    default=False)

# Exported mesh file formats
bpy.types.Scene.NMV_ExportedMeshFormat = bpy.props.EnumProperty(
    items=[(nmv.enums.Meshing.ExportFormat.PLY,
            'Stanford (.ply)',
            'Export the mesh to a .ply file'),
           (nmv.enums.Meshing.ExportFormat.OBJ,
            'Wavefront (.obj)',
            'Export the mesh to a .obj file'),
           (nmv.enums.Meshing.ExportFormat.STL,
            'Stereolithography CAD (.stl)',
            'Export the mesh to an .stl file'),
           (nmv.enums.Meshing.ExportFormat.BLEND,
            'Blender File (.blend)',
            'Export the mesh as a .blend file')],
    name='Format', default=nmv.enums.Meshing.ExportFormat.PLY)
