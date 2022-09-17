import subprocess
import psutil
import platform
import csv
from datetime import datetime
import os


class systemDetails():
    """ Constructor and initializing the class """

    def __init__(self):

        """ System Headings  """
        self.headings = ['System:', 'Host Name:',
                          'IP Address:', 'Kernel:',
                          'Architecture:', 'CPU Cores',
                          'CPU Usage:', 'Total RAM:',
                          'RAM Usage:', 'Last Reboot:', 'UpTime:']

    def generate_html(self):

        """ Extract IP4 Address with the subprocess libary """
        self.ps = subprocess.Popen(('hostname', '--all-ip-addresses'), stdout=subprocess.PIPE)
        self.output = subprocess.check_output(('cut', '-d', ' ', '-f', '1'), stdin=self.ps.stdout)
        self.ps.wait()

        # Remove any white space or invalid characters
        self.ipaddr = str(self.output, 'utf-8').strip('\n')

        """ Last Reboot Time """
        self.boot_time_timestamp = psutil.boot_time()
        self.bt = datetime.fromtimestamp(self.boot_time_timestamp)

        """ System Up Time """
        self.uptime = subprocess.check_output(['uptime'])
        self.uptime = str(self.uptime, 'utf-8').strip('\n')

        """RAM Usage """
        # Get the system memory using psutil and convert it to a dictionary
        dict(psutil.virtual_memory()._asdict())

        # you can then calculate percentage of available memory
        # Total Ram in Gigabytes
        self.totalram = psutil.virtual_memory().total
        self.raminGB = self.totalram / (1024. ** 3)
        self.raminGB = "%.2f" % self.raminGB + 'GB'

        # Available RAM
        self.getmem = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
        self.raminuse = 100 - self.getmem
        self.getmem = "%.2f" % self.getmem + '%'
        # print(f"Ram Available: {self.getmem}")
        self.raminuse = "%.2f" % self.raminuse + '%'

        # CPU Percentage Usage
        self.cpucorecount = psutil.cpu_count(logical=True)
        self.getcpu = psutil.cpu_percent(1)
        self.cpuusge = str(self.getcpu)
        self.cpuusge = self.cpuusge + '%'

        self.uname = platform.uname()
        self.systemdetails = [self.uname.system, self.uname.node,
        self.ipaddr, self.uname.release, self.uname.machine,
        self.cpucorecount, self.cpuusge, self.raminGB, self.raminuse, self.bt, self.uptime]

        """Create the html file cycling through the headings and data """
        with open("System_Details.html", "w") as html_file:
            print("<html><Title>System Details</Title>", file=html_file)
            print("<style>", file=html_file)
            print("th {border:1px solid #095484;}", file=html_file)
            print("td {border:1px groove #1c87c9;}", file=html_file)
            print("</style>", file=html_file)
            print("<table>", file=html_file)

            for title, data in zip(self.headings, self.systemdetails):
                print(f"<tr><th>{title}</th><td>{data}</td></td>", file=html_file)

            print("</table>", file=html_file)
            print("</html>", file=html_file)
            html_file.close()

            """Create a .csv spreadsheet file """

            with open('systemdetails.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                # write system headings
                writer.writerow(self.headings)
                # write systemdetails
                writer.writerow(self.systemdetails)
                f.close()
