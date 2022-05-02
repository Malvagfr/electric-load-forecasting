#############################################################################################################################
#                                                                                                                           #                       
#                                                   Electric load forecasting                                               #     
#                                                                                                                           #
#                                             Ironhack Data Part Time --> Nov-2021                                          #
#                                                                                                                           #
#############################################################################################################################  

###################################################### Modules import #######################################################
from modules.data_extraction import data_extractor_bank_holidays as de_bh
from modules.data_extraction import data_extractor_electricity_demand as de_ed
from modules.data_extraction import data_extractor_population as de_po
from modules.data_extraction import data_extractor_temperature as de_te
from modules.data_transformation import data_transformation as dt

###################################################### Main pipeline function ################################################
def main():
    # Data extraction of each SOT
    #de_bh.extract_bank_holidays()
    #de_ed.extract_electric_demand()
    #de_po.extract_population()
    #de_te.extract_temperature()

    dt.data_transformation()

    # Data transformation


###################################################### Pipeline execution #####################################################
if __name__ == '__main__':
    main()