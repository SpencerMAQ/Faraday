#!/usr/bin/env python3
# Faraday: A Dynamo Plugin (GPL)
# started by Michael Spencer Quinto <https://github.com/SpencerMAQ>
#
# This file is part of Faraday.
#
# You should have received a copy of the GNU General Public License
# along with Faraday; If not, see <http://www.gnu.org/licenses/>.
#
# @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>

# py 3.6

# ------------------ CAUTION! ------------------ #

# DO NOT RUN WHILE DYNAMO IS RUNNING ANY SCRIPT AND USING
# ANY OF THE FILES!! MAY CAUSE FILES TO BECOME CORRUPT!

# Can be used if Dynamo is IDLE

# ------------------ CAUTION! ------------------ #

# TODO: Make this a PyQT script???
# TODO: (include in PyQt but already start including even w/o):
# print out which files would be changed if files already exist, ask for
# user verification

# TODO: try to un-nest the copy function by making MODE a parameter

import os
import shutil
import time


def copy_files(src, dst, dyf=False, nodesrc=True, faradcore=True):
    """Copies files from Dynamo packages folder (e.g. Faraday)
    into the git folder for version control

    The typical workflow would be to edit the python code inside github
    run this script to copy the .py files to the package folder
    Then rebuild the dyf files in Dynamo
    Lastly, recopy the dyf files from Package folder to Github folder

    Mode 1:     Dynamic mode
                copy .py (Faraday/src to ~extra/nodesrc) files from Github
                including Faraday/faradaycore to ~extra/faradaycore

    Mode 2:     Static mode
                copy .py (Faraday/src to ~extra/nodesrc) files from Github
                including Faraday/faradaycore to ~extra/faradaycore

    Mode 3:     Always Static
                copy all DYFs from Packages/Farad/dyf to Github/Faraday/dyf
                DON'T USE THIS MODE WITH DYNAMIC UPDATE!

    Args:
        src:            Package source
        dst:            Github destination repo folder
        dyf:            True to copy dyf files
        nodesrc:        copy files from Dynamo's extra folder to 'src'
        faradcore:      ladybug source dode
        dynamic:        Script runs for 4 hours, automatically
                        checks if files have been modified
    """

    mode_paths_dict =   {
        'dyf':      {
                        'base_src_fldr':    r'dyf',
                        'base_dst_fldr':    r'dyf',
                        'file_extn':        r'.dyf'
                    },

        'nodesrc': {
                        'base_fldr':        r'src',
                        'base_dst_fldr':    r'extra/nodesrc',
                        'file_extn':        r'.py'
                    },

        'faradcore':{
                        'base_fldr':        r'faradaycore',
                        'base_dst_fldr':    r'extra/faradaycore',
                        'file_extn':        r'.py'
                    }
         }

    assert os.path.isdir(src)
    assert os.path.isdir(dst)

    os.chdir(src)
    copied_files = []

    def __copy(base_src_folder, base_dst_fldr, file_extnsn):
        """Actual copy
        Dynamically sets the paths and filetypes based on the dict
        Note: can't un-nest this function because `if dyf` and
        `if nodesrc` have different directories

        Args:
            file_extnsn:    .py or .dyf
        """

        src_files = (f for f in os.listdir(base_src_folder) if f.endswith(file_extnsn))

        os.chdir(dst)
        dst_files = list(f for f in os.listdir(base_dst_fldr) if f.endswith(file_extnsn))

        for f in src_files:
            src_file_path = os.path.join(src, r'{}/{}'.format(base_src_fldr, f))
            dst_path = os.path.join(dst, base_dst_fldr)

            # if file already exists at dst, compute modf time
            if f in dst_files:
                src_modf_time = os.path.getmtime(src_file_path)

                # lookup the same f name in dst_files
                dst_f = dst_files[list(dst_files).index(f)]
                dst_modf_time = os.path.getmtime(os.path.join(dst_path, dst_f))

                if src_modf_time > dst_modf_time:
                    copied_file = shutil.copy2(src_file_path,
                                               dst_path)

                    copied_files.append(os.path.basename(copied_file))

            elif f not in dst_files:
                copied_file = shutil.copy2(src_file_path,
                                           dst_path)

                copied_files.append(os.path.basename(copied_file))

        copied_files.append('\n')


    if dyf:
        mode            = mode_paths_dict['dyf']

        base_src_fldr   = mode['base_src_fldr']
        base_dst_fldr   = mode['base_dst_fldr']
        file_xtn        = mode['file_extn']

        __copy(
            base_src_folder=base_src_fldr,
            base_dst_fldr=base_dst_fldr,
            file_extnsn=file_xtn)

    # TODO: TEST
    if nodesrc:
        mode = mode_paths_dict['nodesrc']

        base_src_fldr = mode['base_src_fldr']
        base_dst_fldr = mode['base_dst_fldr']
        file_xtn = mode['file_extn']

        __copy(
            base_src_folder=base_src_fldr,
            base_dst_fldr=base_dst_fldr,
            file_extnsn=file_xtn)

    # TODO: TEST
    if faradcore:
        mode = mode_paths_dict['faradcore']

        base_src_fldr = mode['base_src_fldr']
        base_dst_fldr = mode['base_dst_fldr']
        file_xtn = mode['file_extn']

        __copy(
            base_src_folder=base_src_fldr,
            base_dst_fldr=base_dst_fldr,
            file_extnsn=file_xtn)

    print(copied_files)

    # if nodesrc:
    #     copied_files = []
    #     nodesrc_py_files = (f for f in os.listdir(r'src') if f.endswith(r'.py'))
    #
    #     os.chdir(dst)
    #     nodesrc_dst_files = list(f for f in os.listdir(r'extra\nodesrc')
    #                              if f.endswith(r'.py')
    #                              )
    #
    #     for f in nodesrc_py_files:
    #         ndsrc_file_src = os.path.join(src, r'src\{}'.format(f))
    #         ndsrc_dest_path = os.path.join(dst, r'extra\nodesrc')
    #
    #         if f in nodesrc_dst_files:
    #             nodesrc_py_modf_time = os.path.getmtime(
    #                                                     os.path.join(
    #                                                         src,
    #                                                         r'src\{}'.format(f))
    #                                                     )
    #
    #             dest_f = nodesrc_dst_files[list(nodesrc_dst_files).index(f)]
    #             dst_f_modf_time = os.path.getmtime(
    #                                                os.path.join(
    #                                                    dst, r'extra\nodesrc'.format(dest_f))
    #                                                )
    #
    #             if nodesrc_py_modf_time > dst_f_modf_time:
    #                 copied_file = shutil.copy2(ndsrc_file_src,
    #                                            ndsrc_dest_path)
    #
    #                 copied_files.append(os.path.basename(copied_file))
    #
    #         elif f not in nodesrc_dst_files:
    #             copied_file = shutil.copy2(ndsrc_file_src,
    #                                        ndsrc_dest_path)
    #
    #             copied_files.append(os.path.basename(copied_file))
    #
    #     print('copied nodesrc: {}'.format(copied_files))


if __name__ == '__main__':
    """Script will run for a max time for 4 hrs, then will automatically
    kill itself
    
    Script copies changed files (depending on the direction specified)
    every 20 seconds
    """

    # TODO: Test dynamic
    # Mode 1 (Dynamic copy all node python and src files)
    mode_1 = False  # dynamic
    mode_2 = False  # nodesrc, core static
    mode_3 = True   # dyf, static

    # TODO: Test on actual directory
    # choose what src and dst are depending on mode, for mode 3: from Dynamo dyf to Github
    _src        = r'D:\Libraries\Documents\GitHub\Faraday' if(mode_1 or mode_2) else \
                    r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\1.3\packages\Faraday'
    _dst        = r'C:\Users\Mi\AppData\Roaming\Dynamo\Dynamo Revit\1.3\packages\Faraday' if(mode_1 or mode_2) else \
                    r'D:\Libraries\Documents\GitHub\Faraday'

    _src = r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\Github\Faraday' if (mode_1 or mode_2) else \
            r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\packages\Faraday'
    _dst = r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\packages\Faraday' if (mode_1 or mode_2) else \
            r'D:\TeMP\1_!_!_!_TEMP\z_python dynamic file copy\Github\Faraday'

    print('src = {}, dst = {}'.format(_src, _dst))

    _dyf        = True if mode_3 else False
    _nodesrc    = False if mode_3 else True
    _faradcore  = False if mode_3 else True
    _dynamic    = True if mode_1 else False

    first_called = time.time()

    while True:
        copy_files(src=_src,
                   dst=_dst,
                   dyf=_dyf,
                   nodesrc=_nodesrc,
                   faradcore=_faradcore)

        if not _dynamic:
            break

        time.sleep(20)
        last_called = time.time()

        if last_called - first_called == 14400:
            break
