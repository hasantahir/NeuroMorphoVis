####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
import math

# Internal imports
import neuromorphovis as nmv
from neuromorphovis.analysis import AnalysisItem
from neuromorphovis.analysis import *
import neuromorphovis.skeleton



####################################################################################################
# @compute_arbor_total_length
####################################################################################################
def compute_arbor_total_length(arbor):
    """Computes the total length of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The total length of the arbor in um.
    """

    # A list that will contains the lengths of all the sections along the arbor
    sections_lengths = list()

    # Compute the length of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_lengths,
          sections_lengths])

    # Total arbor length
    arbor_total_length = 0.0

    # Iterate and sum up all the sections lengths
    for length in sections_lengths:

        # Add to the arbor length
        arbor_total_length += length

    # Return the total section length
    return arbor_total_length


####################################################################################################
# @compute_arbor_total_surface_area
####################################################################################################
def compute_arbor_total_surface_area(arbor):
    """Computes the total surface area of the given arbor.

    :param arbor:
        A given arbor to analyze.
    :return:
        The total surface area of the arbor in um squared.
    """

    # A list that will contains the surface areas of all the sections along the arbor
    sections_surface_areas = list()

    # Compute the surface area of each section individually
    nmv.skeleton.ops.apply_operation_to_arbor(
        *[arbor,
          nmv.analysis.compute_sections_surface_areas_from_segments,
          sections_surface_areas])

    # Total arbor length
    arbor_total_surface_area = 0.0

    # Iterate and sum up all the sections surface areas
    for surface_area in sections_surface_areas:

        # Add to the arbor length
        arbor_total_surface_area += surface_area

    # Return the total section surface area
    return arbor_total_surface_area














####################################################################################################
# @compute_segments_length
####################################################################################################
def compute_segments_length_with_annotations(section,
                                             segments_length_list):
    """Computes the length of each segment along the given section and annotate the result with the
    data of the segments for extended analysis. The results are appends the to the given list.

    :param section:
        A given section to be analyzed.
    :param segments_length_list:
        The list where the computed lengths will be appended to.
    """

    # Iterate over each segment in the section
    for i in range(len(section.samples) - 1):

        # Retrieve the points along each segment on the section
        point_0 = section.samples[i].point
        point_1 = section.samples[i + 1].point

        # Compute the segment length
        segment_length = (point_1 - point_0).length

        #


        # Append it to the list
        segments_length_list.append(segment_length)



