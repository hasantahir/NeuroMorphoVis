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

# Internal imports
from neuromorphovis.analysis.structs import AnalysisItem
from neuromorphovis.analysis.kernels.morphology import *


####################################################################################################
# A list of all the analysis items (or kernels) that will applied on the morphology skeleton
####################################################################################################
ui_analysis_items = [

    ################################################################################################
    # Samples-related items
    ################################################################################################
    # Total number of samples
    AnalysisItem(variable='TotalNumberSamples',
                 name='Total # of Samples',
                 kernel=kernel_total_number_samples,
                 description='The total number of samples',
                 data_format='INT'),

    # Minimum number of samples per section
    AnalysisItem(variable='MinNumberSamplePerSection',
                 name='Min. # Samples / Section',
                 kernel=kernel_minimum_number_samples_per_section,
                 description='The least number of samples per section',
                 data_format='INT'),

    # Maximum number of samples per section
    AnalysisItem(variable='MaxNumberSamplePerSection',
                 name='Max. # Samples / Section',
                 kernel=kernel_maximum_number_samples_per_section,
                 description='The largest number of samples per section',
                 data_format='INT'),

    # Average number of samples per section
    AnalysisItem(variable='AvgNumberSamplePerSection',
                 name='Avg. # Samples / Section',
                 kernel=kernel_average_number_samples_per_section,
                 description='The Average number of samples per  section',
                 data_format='INT'),

    ################################################################################################
    # Length-related items
    ################################################################################################
    # Total length
    AnalysisItem(variable='TotalLength',
                 name='Total Length',
                 kernel=kernel_total_length,
                 description='Total length',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Minimum section length
    AnalysisItem(variable='MinSectionLength',
                 name='Min. Section Length',
                 kernel=kernel_minimum_section_length,
                 description='The length of the shortest section',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Maximum section length
    AnalysisItem(variable='MaxSectionLength',
                 name='Max. Section Length',
                 kernel=kernel_maximum_section_length,
                 description='The length of the shortest section',
                 data_format='FLOAT',
                 unit='LENGTH'),

    # Average section length
    AnalysisItem(variable='AvgSectionLength',
                 name='Avg. Section Length',
                 kernel=kernel_average_section_length,
                 description='Average section length',
                 data_format='FLOAT',
                 unit='LENGTH'),
]

