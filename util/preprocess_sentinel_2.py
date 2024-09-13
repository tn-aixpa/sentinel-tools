import platform
from typing import List 
from util.command_execution import CommandExecution
from util.helper import get_all_files_name_in_dir
from enum import Enum

from util.input_sentinel_class import InputSentinelClass

class TypeElaborations(Enum):
    # ['NORMDIFF','NDVI','EVI','NDWI','NDSI','NBR']
    NORDIFF='normDiff'
    NDVI='NDVI'
    EVI='EVI'
    NDWI='NDWI'
    NDSI='NDSI'
    NBR='NBR'

def execute_snap(snap_command:List[str]):
    exe = CommandExecution(snap_command)
    coherence_res = exe.execute()
    return coherence_res
  
def start_executions(download_parameters: InputSentinelClass= None, products_dir: str=None,output_dir=None):
  if download_parameters.is_sentinel2():
      import os
      snap_commands = []
      snap_graph_path = os.path.join("assets","bandmath.xml")
      snap_graph_path_rgb = os.path.join("assets","bandstack.xml")
      flist = [name_f for name_f in get_all_files_name_in_dir(products_dir)] # if name_f.find(".dim")>=0
      for image_path in flist:
          #new_image_fpath = os.path.join(products_dir,image_fpath)
          new_image_fpath = os.path.join(products_dir,image_path)
          for command in download_parameters.sentinel2Param.rgb_commands:
              # RGB elaborations
              output_dir_rgb = os.path.join(output_dir,command['name'])
              snap_exec = bandstack_snap_cmd(new_image_fpath,command['value'],output_dir=output_dir_rgb,snap_graph_path=snap_graph_path_rgb)
              snap_commands.append(snap_exec)
          for command_value in download_parameters.sentinel2Param.bandmath:
              # bandmath elaborations
              output_dir_bandmath = os.path.join(output_dir,command_value)
              snap_exec =  bandmath_snap_cmd(new_image_fpath,command_value,[],output_dir_bandmath,snap_graph_path)
              snap_commands.append(snap_exec)
          for command in download_parameters.sentinel2Param.norm_diff:
              # bandmath_custom elaborations
              output_dir_bandmath = os.path.join(output_dir,command['name'])
              snap_exec =  bandmath_snap_cmd(new_image_fpath,command_value,command['value'],output_dir_bandmath,snap_graph_path)
              snap_commands.append(snap_exec)
  else:
      raise(Exception("You are trying to execute sentinel2 preprocessing but inserted sentinel1 as sentinelType!!"))
  return snap_commands

#===# NEW
def bandstack_snap_cmd(input_fpath, bands, output_dir, snap_graph_path):
    """
    Returns the SNAP command to stack three bands for RGB visualization. 
    
    :param input_fpath:     Fullfilepath to the target image product
    :bands:                 List of three strings naming the bands to stack on top of each other. Example: ['B4','B3','B2'] 
    :param output_dir:      Fulldirpath to the directory where RGB image should be saved (SNAP processing)
    :param snap_graph_path: Fullfilepath to the SNAP graph file: s2bandstack.xml (mazanetti@fbk.eu)
    
    """

    import os
    
    basename = os.path.basename(input_fpath).replace('.zip','_{}.tif'.format(''.join(bands)))
    output_fpath = os.path.join(output_dir,basename)

    snap_cmd = 'gpt {} -Pinput_fpath={} -Pbands={} -Poutput_fpath={}'.format(
                  snap_graph_path,
                  input_fpath,
                  ','.join(bands),
                  output_fpath)
    
    return snap_cmd

#===# NEW
def bandmath_snap_cmd(input_fpath, index, bands, output_dir, snap_graph_path):
    """
    Returns the SNAP command to launch various bandmath calculations. 
    
    :param input_fpath:     Fullfilepath to the target image product
    :index:                 String, one of ['NORMDIFF','NDVI','EVI','NDWI','NDSI','NBR']
    :param bands:           List of two strings naming the bands to put in the BandMath formula. Example: ['B8','B4']
    :param output_dir:      Fulldirpath to the directory where NDI files should be saved (SNAP processing)
    :param snap_graph_path: Fullfilepath to the SNAP graph file: s2bandmath.xml (mazanetti@fbk.eu)
    
    """

    import os
    
    if index=='NORMDIFF':   
      basename = os.path.basename(input_fpath).replace('.zip','_NDI({},{}).tif'.format(bands[0],bands[1]))
      if platform.system() == "Windows":
          expr = '({abundant}-{absorber})/({abundant}+{absorber})'.format(abundant=bands[0],absorber=bands[1])
      else:
          expr = '\({abundant}-{absorber}\)/\({abundant}+{absorber}\)'.format(abundant=bands[0],absorber=bands[1])  
      band_name = 'ndi({},{})'.format(bands[0],bands[1])
    
    elif index=='NDVI':
      basename = os.path.basename(input_fpath).replace('.zip','_NDVI.tif')
      if platform.system() == "Windows":
        expr = '(B8-B4)/(B8+B4)'
      else:
        expr = '\(B8-B4\)/\(B8+B4\)'
      band_name = 'ndvi'
    
    elif index=='EVI':  
      basename = os.path.basename(input_fpath).replace('.zip','_EVI.tif')
      if platform.system() == "Windows":
        expr = '(2.5*(B8-B4)/((B8+6.0*B4-7.5*B2)+1))'
      else:
        expr = '\(2.5*\(B8-B4\)/\(\(B8+6.0*B4-7.5*B2\)+1\)\)'
      band_name = 'evi'
    
    elif index=='NDWI':
      basename = os.path.basename(input_fpath).replace('.zip','_NDWI.tif')
      if platform.system() == "Windows":
        expr = '(B3-B8)/(B3+B8)'
      else:
        expr = '\(B3-B8\)/\(B3+B8\)'
      
      band_name = 'ndwi'

    elif index=='NDSI':
      basename = os.path.basename(input_fpath).replace('.zip','_NDSI.tif')
      if platform.system() == "Windows":
        expr = '(B3/B11)'
      else:
        expr = '\(B3/B11\)'
      band_name = 'ndsi'
      
    elif index=='NBR':
      basename = os.path.basename(input_fpath).replace('.zip','_NBR.tif')
      if platform.system() == "Windows":
        expr = '(B8-B12)/(B8+B12)'
      else:
        expr = '\(B8-B12\)/\(B8+B12\)'
      band_name = 'nbr'
    
    output_fpath = os.path.join(output_dir,basename)
    
    snap_cmd = 'gpt {} -Pinput_fpath={} -Pband_name={} -Pexpression={} -Poutput_fpath={}'.format(
                  snap_graph_path,
                  input_fpath,
                  band_name,
                  expr,
                  output_fpath)
    
    return snap_cmd