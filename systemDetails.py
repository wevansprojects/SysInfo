import os
import subprocess
import psutil
import platform
from datetime import datetime


class SystemDetails:
    """ Constructor and initializing the class """

    def get_size(self, bytes, suffix="B"):
        self.bytes = bytes
        factor = 1024

        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    def details(self):
        print("=" * 30, "System Information", "=" * 20)
        self.uname = platform.uname()
        self.extractips = subprocess.check_output(['hostname', '--all-ip-addresses'])
        self.ipaddr = str(self.extractips, 'utf-8').strip('\n')
        print(f"System: {self.uname.system}")
        print(f"Node Name: {self.uname.node}")
        print(f"Ip 4/6 Address: {self.ipaddr}")
        print(f"Release: {self.uname.release}")
        print(f"Version: {self.uname.version}")
        print(f"Machine: {self.uname.machine}")
        print(f"Processor: {self.uname.processor}")
        print("=" * 70)

    def last_reboot_time(self):
        """ Last Reboot Time """
        self.boot_time_timestamp = psutil.boot_time()
        self.bt = datetime.fromtimestamp(self.boot_time_timestamp)
        print(f"Boot Time: {self.bt}")
        print("=" * 70)

    def cpu_details(self):
        """ CPU Information """
        print("=" * 30, "CPU Info", "=" * 30)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        self.cpu_percent_cores = psutil.cpu_percent(interval=2, percpu=True)
        self.avg = sum(self.cpu_percent_cores) / len(self.cpu_percent_cores)
        self.cpu_percent_total_str = ('%.2f' % self.avg) + '%'
        print("Total cores:", psutil.cpu_count(logical=True))
        # CPU frequencies
        self.cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {self.cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {self.cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {self.cpufreq.current:.2f}Mhz")
        # CPU usage
        print('Total CPU Usage: {}'.format(self.cpu_percent_total_str))
        print("=" * 70)

    def ram_utilisation(self):
        """ RAM Utilisation  """
        print("=" * 30, "RAM Utilisation", "=" * 23)
        # get the memory details
        self.svmem = psutil.virtual_memory()
        print(f"Total: {self.get_size(self.svmem.total)}")
        print(f"Available: {self.get_size(self.svmem.available)}")
        print(f"Used: {self.get_size(self.svmem.used)}")
        print(f"Percentage: {self.svmem.percent}%")
        print("=" * 30, "SWAP", "=" * 34)
        # get the swap memory details (if exists)
        self.swap = psutil.swap_memory()
        print(f"Total: {self.get_size(self.swap.total)}")
        print(f"Free: {self.get_size(self.swap.free)}")
        print(f"Used: {self.get_size(self.swap.used)}")
        print(f"Percentage: {self.swap.percent}%")
