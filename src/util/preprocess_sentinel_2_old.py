import platform
from typing import List
from util.command_execution import CommandExecution
from util.helper import get_all_files_name_in_dir

class CoupleBase():
    custom: bool
    name: str
    acronim: str
    list_products: List[str]


def execute_snap(snap_command:List[str]):
    exe = CommandExecution(snap_command)
    coherence_res = exe.execute()
    return coherence_res

def upsample_snap_cmd(image_fpath, output_dir, snap_graph_path):
    """
    Returns the SNAP command to upsample all bands to 10m resolution. 
    
    :param image_fpath:     Fullfilepath to the target image product
    :param output_dir:      Fulldirpath to the directory where upsampled image should be saved (SNAP processing)
    :param snap_graph_path: Fullfilepath to the SNAP graph file: upsample.xml (mazanetti@fbk.eu)
    
    """
    import os
    basename = os.path.basename(image_fpath).replace('.zip','.dim')
    result_fpath = os.path.join(output_dir,basename)
    snap_cmd = 'gpt {} -Pimage_fpath={} -Presult_fpath={}'.format(
                snap_graph_path,
                image_fpath,
                result_fpath)
    return snap_cmd

def execute_preprocessing_sentinel2(operation:List[CoupleBase],products_dir:str,output_dir):
    from glob import glob
    import os
    #print(products_dir)
    flist = [name_f for name_f in get_all_files_name_in_dir(products_dir) if name_f.find(".dim")>=0]
    #flist = glob(products_dir+"*",recursive=True)
    #print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&: ", flist)
    norm_diff_elabs =[i for i in operation if not i.custom]
    #print(norm_diff_elabs)
    custom_elabs =[i for i in operation if i.custom]
    print("RGB elabs", custom_elabs)
    snap_commands = []
    for bandsCouple in norm_diff_elabs:
        full_name_dir = bandsCouple.name + "_" + bandsCouple.acronim
        for eelab in bandsCouple.list_products:
            full_name_dir+= "_" + eelab
        new_output_dir = os.path.join(output_dir,full_name_dir)
        for image_fpath in flist:
            new_image_fpath = os.path.join(products_dir,image_fpath)
            snap_graph_path = os.path.join("assets","bandmath.xml")
            snap = expression_snap_cmd(new_image_fpath,bandsCouple.name,bandsCouple.list_products,new_output_dir,snap_graph_path)
            snap_commands.append(snap)
    snap_graph_path_rgb = os.path.join("assets","bandstack.xml")
    for custom_el in custom_elabs:
        """RGB elabs"""
        full_name_dir = custom_el.name + "_" + custom_el.acronim
        for eelab in custom_el.list_products:
            full_name_dir+= "_" + eelab
        new_output_dir = os.path.join(output_dir,full_name_dir)
        for image_fpath in flist:
            new_image_fpath = os.path.join(products_dir,image_fpath)
            snap = stackrgb_snap_cmd(new_image_fpath,custom_el.list_products,new_output_dir,snap_graph_path_rgb)
            snap_commands.append(snap)
        pass
    print(f"Snap commands: {snap_commands}")
    result = execute_snap(snap_commands)
    return result

def stackrgb_snap_cmd(image_fpath, bands, output_dir, snap_graph_path):
    """
    RGB and false RBG
    Returns the SNAP command to stack three bands for RGB (true or false) visualization. 
    
    :param image_fpath:     Fullfilepath to the target image product
    :bands:                 List of three strings naming the bands to stack on top of each other. Example: ['B4','B3','B2'] 
    :param output_dir:      Fulldirpath to the directory where RGB image should be saved (SNAP processing)
    :param snap_graph_path: Fullfilepath to the SNAP graph file: bandstack.xml (mazanetti@fbk.eu)
    
    """

    import os
    
    basename = os.path.basename(image_fpath).replace('.dim','_{}.tif'.format(''.join(bands)))
    result_fpath = os.path.join(output_dir,basename)

    snap_cmd = 'gpt {} -Pimage_fpath={} -Pbands={} -Presult_fpath={}'.format(
                  snap_graph_path,
                  image_fpath,
                  ','.join(bands),
                  result_fpath)
    
    return snap_cmd



#===#
def expression_snap_cmd(image_fpath, index, bands, output_dir, snap_graph_path):
    """
    Returns the SNAP command to launch various index calculations. 
    
    :param image_fpath:     Fullfilepath to the target image product
    :index:                 String, one of ['NORMDIFF','NDSI','EVI']
    :param bands:           List of two strings naming the bands to put in the BandMath formula. Example: ['B8','B4']
    :param output_dir:      Fulldirpath to the directory where NDI files should be saved (SNAP processing)
    :param snap_graph_path: Fullfilepath to the SNAP graph file: bandmath.xml (mazanetti@fbk.eu)
    
    """

    import os
    basename = None
    result_fpath = None
    expr = None
    band_name = None
    if index=='normDiff' or index=='normVegetation' or index=='normWater' or index=='normBurn':
        basename = os.path.basename(image_fpath).replace('.dim','_NORMDIFF_{}_{}.tif'.format(bands[0],bands[1]))
        result_fpath = os.path.join(output_dir,basename)
        if platform.system() == "Windows":
            expr = '({abundant}-{absorber})/({abundant}+{absorber})'.format(abundant=bands[0],absorber=bands[1])
        else:
            expr = '\({abundant}-{absorber}\)/\({abundant}+{absorber}\)'.format(abundant=bands[0],absorber=bands[1])  
        band_name = 'normalized-difference'
      
    elif index=='normSnow':
        basename = os.path.basename(image_fpath).replace('.dim','_NDSI.tif')
        result_fpath = os.path.join(output_dir,basename)
        if platform.system() == "Windows":
            expr = '(B3/B11)'
        else:
            expr = '\(B3/B11\)'
        band_name = 'normalized-difference-snow-index'
      
    elif index=='enhancedVegetation':  
        basename = os.path.basename(image_fpath).replace('.dim','_EVI.tif')
        result_fpath = os.path.join(output_dir,basename)
        if platform.system() == "Windows":
            expr = '(2.5*(B8-B4)/((B8+6.0*B4-7.5*B2)+1))'
        else:
            expr = '\(2.5*\(B8-B4\)/\(\(B8+6.0*B4-7.5*B2\)+1\)\)'
        band_name = 'enhanced-vegetation-index'

    snap_cmd = 'gpt {} -Pimage_fpath={} -Pband_name={} -Pexpression={} -Presult_fpath={}'.format(
                    snap_graph_path,
                    image_fpath,
                    band_name,
                    expr,
                    result_fpath)
    
    return snap_cmd