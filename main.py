from System_Details import System_Details
#from System_Details_To_File import System_Details_To_file
from System_Details_To_File_Simplified import System_Details_Simple

# Main Function to print system details
def main():
    """Print Out System Details To Terminal"""
    sysinfo = System_Details()
    sysinfo.details()
    sysinfo.last_reboot_time()
    sysinfo.cpu_details()
    sysinfo.ram_utilisation()

    """Create HTML File of System Details """
#    sysinfotohtml = System_Details_To_file()
#    sysinfotohtml.generate_html()

    """Create HTML File of System Details """
    sysinfosimple = System_Details_Simple()
    sysinfosimple.generate_html()

if __name__ == "__main__":
    main()