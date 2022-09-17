import os
import subprocess
import psutil
import platform

from datetime import datetime

class System_Details_To_file():
    """ Constructor and initializing the class """

    """To Calculate Memory from Bytes to MB or GB"""
    def get_size(self, bytes, suffix="B"):
        self.bytes = bytes
        factor = 1024

        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def generate_html(self):
        """Generic System Information"""
        self.uname = platform.uname()
        #self.extractips = subprocess.check_output(['hostname', '--all-ip-addresses'])

        """ Extract IP4 Address with the subprocess libary """
        self.ps = subprocess.Popen(('hostname', '--all-ip-addresses'), stdout=subprocess.PIPE)
        self.output = subprocess.check_output(('cut', '-d', ' ', '-f', '1'), stdin=self.ps.stdout)
        self.ps.wait()

        #Remove any white space or invalid characters
        self.ipaddr = str(self.output, 'utf-8').strip('\n')

        """ Last Reboot Time """
        self.boot_time_timestamp = psutil.boot_time()
        self.bt = datetime.fromtimestamp(self.boot_time_timestamp)

        """ CPU Details """
        #Number of Cores
        self.cpu_percent_cores = psutil.cpu_percent(interval=2, percpu=True)
        #CPU Usage as a Percentage
        self.avg = sum(self.cpu_percent_cores) / len(self.cpu_percent_cores)
        self.cpu_percent_total_str = ('%.2f' % self.avg) + '%'
        psutil.cpu_count(logical=True)

        """ RAM Details """
        self.svmem = psutil.virtual_memory()
        #RAM Total
        self.get_size(self.svmem.total)
        #RAM Usage as a percentage
        self.memusage=str(self.svmem.percent) + '%'

        """System Headings  """
        systemheadings = ['System:', 'Host Name:',
                          'IP Address:', 'Kernel:',
                          'Architecture:', 'CPU Cores',
                          'CPU Usage:', 'Total RAM:',
                          'RAM Usage:', 'Last Reboot:']

        """ Extracted List of information """
        self.systemdetails = [self.uname.node,self.uname.system,self.ipaddr,
                              self.uname.release,self.uname.machine,psutil.cpu_count(logical=True),
                              self.cpu_percent_total_str,self.get_size(self.svmem.total),
                              self.memusage,self.bt]

        """Create the html file cycling through the headings and data """
        with open("System_Details.html", "w") as html_file:
            print("<html><Title>System Details</Title>", file=html_file)
            print("<style>", file=html_file)
            print("th {border:1px solid #095484;}", file=html_file)
            print("td {border:1px groove #1c87c9;}", file=html_file)
            print("</style>", file=html_file)
            print("<table>", file=html_file)

            for title, data in zip(systemheadings, self.systemdetails):
                print(f"<tr><th>{title}</th><td>{data}</td></td>", file=html_file)

            print("</table>", file=html_file)
            print("</html>", file=html_file)
            html_file.close()
