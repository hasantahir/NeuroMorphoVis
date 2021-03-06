####################################################################################################
# Copyright (c) 2016 - 2020, EPFL / Blue Brain Project
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


# Internal imports
import nmv.consts
import nmv.analysis
import nmv.utilities


####################################################################################################
# @kernel_total_number_samples
####################################################################################################
def kernel_total_number_samples(morphology):
    """Analyse the total number of samples of the given morphology.

    This analysis accounts for the number of samples of each individual arbor or neurite of the
    morphology and the total number of samples of the entire morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_number_of_samples_of_arbor,
                                      nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_number_samples_per_section
####################################################################################################
def kernel_minimum_number_samples_per_section(morphology):
    """Analyses the minimum number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_minimum_samples_count_of_arbor,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_distance_from_initial_sample_to_origin
####################################################################################################
def kernel_distance_from_initial_sample_to_origin(morphology):
    """Computes the distance between the first sample along the arbor and the soma.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_first_sample_distance_to_soma,
                                      nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_number_samples_per_section
####################################################################################################
def kernel_maximum_number_samples_per_section(morphology):
    """Analyses the maximum number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(morphology,
                                      nmv.analysis.compute_maximum_samples_count_of_arbor,
                                      nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_number_samples_per_section
####################################################################################################
def kernel_average_number_samples_per_section(morphology):
    """Analyses the average number of samples per section of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_number_samples_per_section_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_number_zero_radius_samples
####################################################################################################
def kernel_number_zero_radius_samples(morphology):
    """Find the number of zero-radii samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_number_of_zero_radius_samples_per_section_of_arbor,
        nmv.analysis.compute_total_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_sample_radius
####################################################################################################
def kernel_minimum_sample_radius(morphology):
    """Find the minimum radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_sample_radius_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_sample_radius
####################################################################################################
def kernel_maximum_sample_radius(morphology):
    """Find the minimum radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_sample_radius_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_sample_radius
####################################################################################################
def kernel_average_sample_radius(morphology):
    """Find the average radius of the samples of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_sample_radius_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)


####################################################################################################
# @kernel_minimum_daughter_ratio
####################################################################################################
def kernel_minimum_daughter_ratio(morphology):
    """Find the minimum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_daughter_ratio_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_maximum_daughter_ratio
####################################################################################################
def kernel_maximum_daughter_ratio(morphology):
    """Find the maximum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_daughter_ratio_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_daughter_ratio
####################################################################################################
def kernel_average_daughter_ratio(morphology):
    """Find the average daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_daughter_ratio_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_minimum_parent_daughter_ratio
####################################################################################################
def kernel_minimum_parent_daughter_ratio(morphology):
    """Find the minimum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_parent_daughter_ratio_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_maximum_parent_daughter_ratio
####################################################################################################
def kernel_maximum_parent_daughter_ratio(morphology):
    """Find the maximum daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_parent_daughter_ratio_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_parent_daughter_ratio
####################################################################################################
def kernel_average_parent_daughter_ratio(morphology):
    """Find the average daughter ratio of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_parent_daughter_ratio_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology_and_ignore_zero)


####################################################################################################
# @kernel_minimum_partition_asymmetry
####################################################################################################
def kernel_minimum_partition_asymmetry(morphology):
    """Find the minimum partition asymmetry of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_minimum_partition_asymmetry_of_arbor,
        nmv.analysis.compute_minimum_analysis_result_of_morphology)


####################################################################################################
# @kernel_maximum_partition_asymmetry
####################################################################################################
def kernel_maximum_partition_asymmetry(morphology):
    """Find the maximum partition asymmetry of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_maximum_partition_asymmetry_of_arbor,
        nmv.analysis.compute_maximum_analysis_result_of_morphology)


####################################################################################################
# @kernel_average_partition_asymmetry
####################################################################################################
def kernel_average_partition_asymmetry(morphology):
    """Find the average partition asymmetry of the given morphology.

    :param morphology:
        A given morphology skeleton to analyse.
    :return:
        The result of the analysis operation.
    """

    return nmv.analysis.invoke_kernel(
        morphology,
        nmv.analysis.compute_average_partition_asymmetry_of_arbor,
        nmv.analysis.compute_average_analysis_result_of_morphology)
