####################################################################################################
# Copyright (c) 2016 - 2019, EPFL / Blue Brain Project
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

# System imports
import copy

# Internal imports
import nmv.mesh
import nmv.enums
import nmv.skeleton
import nmv.consts
import nmv.geometry
import nmv.scene
import nmv.shading


####################################################################################################
# @DisconnectedSegmentsBuilder
####################################################################################################
class DisconnectedSegmentsBuilder:
    """Builds and draws the morphology as a series of disconnected segments for analysis.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Morphology
        self.morphology = copy.deepcopy(morphology)

        # System options
        self.options = copy.deepcopy(options)

        # All the reconstructed objects of the morphology, for example, poly-lines, spheres etc...
        self.morphology_objects = []

        # A list of the colors/materials of the soma
        self.soma_materials = None

        # A list of the colors/materials of the axon
        self.axons_materials = None

        # A list of the colors/materials of the basal dendrites
        self.basal_dendrites_materials = None

        # A list of the colors/materials of the apical dendrite
        self.apical_dendrites_materials = None

        # A list of the colors/materials of the articulation spheres
        self.articulations_materials = None

        # An aggregate list of all the materials of the skeleton
        self.skeleton_materials = list()

    ################################################################################################
    # @create_single_skeleton_materials_list
    ################################################################################################
    def create_single_skeleton_materials_list(self):
        """Creates a list of all the materials required for coloring the skeleton.

        NOTE: Before drawing the skeleton, create the materials, once and for all, to improve the
        performance since this is way better than creating a new material per section or segment
        or any individual object.
        """
        nmv.logger.info('Creating materials')

        # Create the default material list
        nmv.builders.morphology.create_skeleton_materials_and_illumination(builder=self)

        # Index: 0 - 1
        self.skeleton_materials.extend(self.soma_materials)

        # Index: 2 - 3
        self.skeleton_materials.extend(self.apical_dendrites_materials)

        # Index: 4 - 5
        self.skeleton_materials.extend(self.basal_dendrites_materials)

        # Index: 6 - 7
        self.skeleton_materials.extend(self.axons_materials)

    ################################################################################################
    # @construct_tree_poly_lines
    ################################################################################################
    def construct_tree_poly_lines(self,
                                  root,
                                  poly_lines_list=[],
                                  branching_order=0,
                                  max_branching_order=nmv.consts.Math.INFINITY,
                                  prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                                  material_start_index=0):
        """Creates a list of poly-lines corresponding to all the sections in the given tree.

        :param root:
            Arbor root, or children sections.
        :param poly_lines_list:
            A list that will combine all the constructed poly-lines.
        :param branching_order:
            Current branching level of the arbor.
        :param max_branching_order:
            The maximum branching level given by the user.
        :param prefix:
            The prefix that is prepended to the name of the poly-line.
        :param material_start_index:
            An index that indicates which material to be used for which arbor.
        """

        # If the section is None, simply return
        if root is None:
            return

        # Increment the branching level
        branching_order += 1

        # Return if we exceed the maximum branching level
        if branching_order > max_branching_order:
            return

        # Get a list of segments poly-lines samples
        segments_poly_lines = nmv.skeleton.get_segments_poly_lines(section=root)

        # Construct the poly-line
        for i, segment_poly_line in enumerate(segments_poly_lines):
            poly_line = nmv.geometry.PolyLine(
                name='%s_%d_%d' % (prefix, branching_order, i),
                samples=segment_poly_line,
                material_index=material_start_index + (i % 2))

            # Add the poly-line to the poly-lines list
            poly_lines_list.append(poly_line)

        # Process the children, section by section
        for child in root.children:
            self.construct_tree_poly_lines(root=child,
                                           poly_lines_list=poly_lines_list,
                                           branching_order=branching_order,
                                           max_branching_order=max_branching_order,
                                           material_start_index=material_start_index)

    ################################################################################################
    # @draw_arbors_as_single_object
    ################################################################################################
    def draw_arbors_as_single_object(self,
                                     bevel_object):
        """Draws all the arbors as a single object.

        :param bevel_object:
            Bevel object used to interpolate the polylines.
        """

        # A list of all the skeleton poly-lines
        skeleton_poly_lines = list()

        # Apical dendrites
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX)

        # Draw the poly-lines as a single object
        morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
            poly_lines=skeleton_poly_lines, object_name=self.morphology.label,
            edges=self.options.morphology.edges, bevel_object=bevel_object,
            materials=self.skeleton_materials)

        # Append it to the morphology objects
        self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @draw_each_arbor_as_single_object
    ################################################################################################
    def draw_each_arbor_as_single_object(self,
                                         bevel_object):
        """Draws each arbor as a single object.

         :param bevel_object:
            Bevel object used to interpolate the polylines.
        """

        # Apical dendrites
        nmv.logger.info('Reconstructing arbors')
        if not self.options.morphology.ignore_apical_dendrites:
            if self.morphology.has_apical_dendrites():
                for arbor in self.morphology.apical_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.apical_dendrite_branch_order,
                        prefix=nmv.consts.Skeleton.APICAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.APICAL_DENDRITE_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Axons
        if not self.options.morphology.ignore_axons:
            if self.morphology.has_axons():
                for arbor in self.morphology.axons:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.axon_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.AXON_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

        # Basal dendrites
        if not self.options.morphology.ignore_basal_dendrites:
            if self.morphology.has_basal_dendrites():
                for arbor in self.morphology.basal_dendrites:
                    nmv.logger.detail(arbor.label)
                    skeleton_poly_lines = list()
                    self.construct_tree_poly_lines(
                        root=arbor,
                        poly_lines_list=skeleton_poly_lines,
                        max_branching_order=self.options.morphology.basal_dendrites_branch_order,
                        prefix=nmv.consts.Skeleton.BASAL_DENDRITES_PREFIX,
                        material_start_index=nmv.enums.Color.BASAL_DENDRITES_MATERIAL_START_INDEX)

                    # Draw the poly-lines as a single object
                    morphology_object = nmv.geometry.draw_poly_lines_in_single_object(
                        poly_lines=skeleton_poly_lines, object_name=arbor.label,
                        edges=self.options.morphology.edges, bevel_object=bevel_object,
                        materials=self.skeleton_materials)

                    # Append it to the morphology objects
                    self.morphology_objects.append(morphology_object)

    ################################################################################################
    # @draw_morphology_skeleton
    ################################################################################################
    def draw_morphology_skeleton(self):
        """Reconstruct and draw the morphological skeleton.

        :return
            A list of all the drawn morphology objects including the soma and arbors.
        """

        nmv.logger.header('Building Skeleton: DisconnectedSegmentsBuilder')

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology and then hide it
        bevel_object = nmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Add the bevel object to the morphology objects because if this bevel is lost we will
        # lose the rounded structure of the arbors
        self.morphology_objects.append(bevel_object)

        # Create the skeleton materials
        self.create_single_skeleton_materials_list()

        # Updating radii
        nmv.skeleton.update_arbors_radii(self.morphology, self.options.morphology)

        # Resample the sections of the morphology skeleton
        nmv.builders.morphology.resample_skeleton_sections(builder=self)

        # Draws each arbor in the morphology as a single object
        self.draw_each_arbor_as_single_object(bevel_object=bevel_object)

        # Draw the soma
        nmv.builders.morphology.draw_soma(builder=self)

        # Transforming to global coordinates
        nmv.builders.morphology.transform_to_global_coordinates(builder=self)

        # Return the list of the drawn morphology objects
        return self.morphology_objects
