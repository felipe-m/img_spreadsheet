import os
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(%(levelname)s - %(message)s')
                    
logger = logging.getLogger(__name__)

def ppm2cvs (filereadname):


    filewritename = os.path.splitext(filereadname)[0] + ".txt"
    file_out = open(filewritename, 'w')
    with open(filereadname,'r') as file_ppm:
        line_i = 1
        header = 1
        header_i = 0
        file_type = None
        file_ncol = None
        file_nline = None
        file_colormax = None
        ncol = 0 # column that is being written to the file
        nline = 0 # line that is being written to the file
        wrtline_l = []
        for line in file_ppm:
            list_line = line.split()
            for elem in list_line:
                #print (elem)
                if elem == '#':
                    break;
                elif header == 1: #we are in the header
                    if file_type == None:
                        if elem == 'P1':
                            file_type = 'P1' # PBM
                            file_colormax = 1
                            wrtline_l.append(file_type)
                        elif elem == 'P2' or elem == 'P3':
                            file_type = elem 
                            wrtline_l.append(file_type)
                        else:
                            logger.error ("File type unknown")
                    elif file_ncol == None:
                        file_ncol = int(elem)
                        wrtline_l.append(elem)
                    elif file_nline == None:
                        file_nline = int(elem)
                        wrtline_l.append(elem)
                        if file_type == 'P1': #PBM
                            header = 0
                            wrtline_l.append('\n')
                            file_out.write(' '.join(wrtline_l))
                            wrtline_l = []
                    elif file_colormax == None:
                        file_colormax = int(elem)
                        wrtline_l.append(elem)
                        header = 0
                        wrtline_l.append('\n')
                        file_out.write(' '.join(wrtline_l))
                        wrtline_l = []
                    else:
                        logger.error("Header error")
                else: # not in the header anymore
                    wrtline_l.append(elem)
                    if ncol == file_ncol-1:
                        wrtline_l.append('\n')
                        # the last element of this line
                        file_out.write(' '.join(wrtline_l))
                        wrtline_l = []
                        ncol = 0
                        nline += 1
                    else:
                        ncol += 1
                        
        if not (ncol == 0 and nline == file_nline):
            logger.error("Error in file or col number")
                        
    file_out.close()
                    
                
           
  


