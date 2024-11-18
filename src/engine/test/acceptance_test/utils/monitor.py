import argparse
import logging
import psutil
from collections import namedtuple
from datetime import datetime
from os.path import isfile
from signal import signal, SIGINT
from sys import platform
from threading import Thread
from time import sleep, time
from subprocess import check_output

logging.basicConfig(filename='monitor.log', level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger('monitor')

def enable_disk_monitoring_win():
    import subprocess
    logger.info("Running diskperf on Windows host")
    cmd = "diskperf -y"
    process = subprocess.Popen(cmd, shell=True)
    if process.returncode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)


if platform == "darwin":
    agentd_state_file = "/Library/Ossec/var/run/xcyber360-agentd.state"
elif platform == "win32":
    agentd_state_file = "C:\\Program Files (x86)\\ossec-agent\\xcyber360-agent.state"
    enable_disk_monitoring_win()
else:
    agentd_state_file = "/var/ossec/var/run/xcyber360-agentd.state"


xcyber360_binaries = {
    "manager": set(["xcyber360-analysisd", "xcyber360-authd", "xcyber360-execd",
                "xcyber360-integratord", "xcyber360-logcollector", "xcyber360-maild",
                "xcyber360-monitord", "xcyber360-syscheckd", "xcyber360-remoted",
                "xcyber360-modulesd", "xcyber360-clusterd", "xcyber360-db", ]),
    "agent": set(["xcyber360-agentd", "xcyber360-execd", "xcyber360-logcollector",
              "xcyber360-syscheckd", "xcyber360-modulesd", ]),
    "winagent": set(["xcyber360-agent.exe", ])
}


def check_binary(binary_list):
    for binary in binary_list:
        for _, binaries in xcyber360_binaries.items():
            if binary in binaries:
                break
        else:
            raise KeyError


def parse_state_file(filename):
    """
    Return a dictionary with the data from a .state
    file generated by Xcyber360
    :params filename: Path of the .state file
    """
    logging.info("Getting statistics data from {}".format(filename))
    data = {}
    with open(filename) as state_file:
        for line in state_file:
            if line.rstrip() and line.rstrip()[0] != '#':
                key, value = line.splitlines()[0].split('=')
                data[key] = value.split("'")[1]
    return data


def get_timestamp():
    """
    Returns a string with the current time stamp as '2019-05-08 16:21:34'
    :returns string
    """
    return datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')


def signal_handler(n_signal, frame):
    logger.info("Exit signal received. Bye!")
    exit(0)


def value_extractor(values):
    """
    Extract a formatted version of the values from the scan.
    :params values: dictionary with all the monitored values
    :returns namedtupled
    """
    Values = namedtuple('Values', ['cpu', 'mem', 'virtual_mem', 'fd',
                        'read_ops', 'write_ops', 'bytes_read', 'bytes_written',
                        'disk_usage', 'uss', 'pss', 'swap'])

    cpu = round(values["current_cpu"], 3)
    mem = values["current_resident_set_size"] / 1024
    virtual_mem = values["current_virtual_memory_usage"] / 1024
    uss = values["current_unique_set_size_memory"] / 1024
    pss = values["current_proportional_set_size_memory"] / 1024
    swap = values["current_swapping_memory"] / 1024
    fd = values["current_file_descriptors"]
    r_ops = values["read_ops"]
    w_ops = values["write_ops"]
    bytes_r = values["bytes_read"]
    bytes_w = values["bytes_written"]
    disk = values["disk_usage"]

    return Values(cpu=cpu, mem=mem, virtual_mem=virtual_mem, fd=fd,
                  read_ops=r_ops, write_ops=w_ops, bytes_read=bytes_r,
                  bytes_written=bytes_w, disk_usage=disk,
                  uss=uss, pss=pss, swap=swap)


def write_csv(data, target, log_file):
    """
    Write a CSV file to store the data collected in the scans
    :param data: dict with the global results
    :param target: specifies which CSV must be generated
    :param log_file: final path to store the CSV file
    """
    header = False

    analysisd_header = ["Timestamp", "Total Events", "Syscheck Events Decoded", "Syscheck EDPS",
                        "Syscollector Events Decoded", "Syscollector EDPS", "Rootcheck Events Decoded",
                        "Rootcheck EDPS", "SCA Events Decoded", "SCA EDPS", "HostInfo Events Decoded", "HostInfo EDPS",
                        "WinEvt Events Decoded", "WinEvt EDPS", "Other Events Decoded", "Other EDPS",
                        "Events processed (Rule matching)", "Events EDPS (Rule matching)", "Events received",
                        "Events dropped",
                        "Syscheck queue", "Syscollector queue", "Rootcheck queue", "SCA queue",
                        "Hostinfo queue", "Winevt queue", "Event queue", "Rule matching queue",
                        "Alerts log queue", "Firewall log queue", "Statistical log queue",
                        "Archives log queue", "Alerts written", "Firewall alerts written", "FTS alerts written"]

    remoted_header = ["Timestamp", "Queue size",
                      "Total Queue size", "TCP sessions", "Events count",
                      "Control messages", "Discarded messages",
                      "Messages sent", "Bytes received"]

    agentd_header = ["Timestamp", "Status", "Last Keepalive",
                     "Last ACK", "Number of generated events", "Number of messages", "Number of events buffered"]

    binaries_header = ['TIMESTAMP', 'PROCESS', 'CPU_PCT', 'RSS_KB',
                       'VMS_KB', 'FD', 'READ_OPS', 'WRITE_OPS', 'DISK_READ_B',
                       'DISK_WRITTEN_B', 'DISK_PCT', 'USS_KB']

    if platform == 'linux':
        binaries_header += ['PSS_KB', 'SWAP_KB']

    if target == "binaries":
        csv_header = binaries_header

    if not isfile(log_file):
        header = True

    with open(log_file, 'a+') as log:

        if header:
            log.write(f'{",".join(csv_header)}\n')

        if target == "binaries":
            logger.info("Writing binary info to {}.".format(log_file))
            for process, values in zip(data.keys(), data.values()):
                formatted_values = value_extractor(values)

                if platform == 'linux':
                    log.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                        get_timestamp(), process,
                        formatted_values.cpu, formatted_values.mem, formatted_values.virtual_mem,
                        formatted_values.fd, formatted_values.read_ops, formatted_values.write_ops,
                        formatted_values.bytes_read, formatted_values.bytes_written, formatted_values.disk_usage,
                        formatted_values.uss, formatted_values.pss, formatted_values.swap))
                else:
                    log.write("{},{},{},{},{},{},{},{},{},{},{},{}\n".format(
                        get_timestamp(), process,
                        formatted_values.cpu, formatted_values.mem, formatted_values.virtual_mem,
                        formatted_values.fd, formatted_values.read_ops, formatted_values.write_ops,
                        formatted_values.bytes_read, formatted_values.bytes_written, formatted_values.disk_usage,
                        formatted_values.uss))


def compute_diff(check_results, process):
    """
    Compute the difference between iterations
    :param check_results: dict with the global results.
    :param process: results from the current check.
    """
    logger.info("Collecting resources usage of {}.".format(process.name()))
    logger.debug("Getting CPU, memory and FDs data.")
    # Load cpu, memory data
    cpu_data = process.cpu_percent(0.1)
    if platform == 'darwin' or platform == 'sunos5':
        memory_data = process.memory_info()
        mem_percent = process.memory_percent()
        fds = process.num_fds()
        logger.debug("Updating CPU, memory and FDs data.")
        check_results[process.name()]["current_cpu"] = cpu_data
        check_results[process.name()]["current_virtual_memory_usage"] = memory_data.vms
        check_results[process.name()]["current_resident_set_size"] = memory_data.rss
        check_results[process.name()]["current_memory_usage"] = mem_percent
        check_results[process.name()]["current_file_descriptors"] = fds
    else:
        memory_data = process.memory_full_info()
        mem_percent = process.memory_percent()
        fds = process.num_fds()
        logger.debug("Updating CPU, memory and FDs data.")
        check_results[process.name()]["current_cpu"] = cpu_data
        check_results[process.name()]["current_virtual_memory_usage"] = memory_data.vms
        check_results[process.name()]["current_resident_set_size"] = memory_data.rss
        check_results[process.name()]["current_memory_usage"] = mem_percent
        check_results[process.name()]["current_file_descriptors"] = fds
        check_results[process.name()]["current_unique_set_size_memory"] = memory_data.uss

    if platform == 'linux':
        check_results[process.name()]["current_proportional_set_size_memory"] = memory_data.pss
        check_results[process.name()]["current_swapping_memory"] = memory_data.swap

    if platform == 'linux' or platform == "win32":
        logger.debug("Getting I/O data.")
        # I/O operations doesn't work by default in Docker's containers
        io_counters = process.io_counters()
        disk_usage_process = io_counters.read_bytes + io_counters.write_bytes
        disk_io_counter = psutil.disk_io_counters()
        disk_total = disk_io_counter.read_bytes + disk_io_counter.write_bytes
        logger.debug("Updating I/O data.")
        check_results[process.name()]["read_ops"] = io_counters.read_count
        check_results[process.name()]["write_ops"] = io_counters.write_count
        check_results[process.name()]["bytes_read"] = io_counters.read_bytes
        check_results[process.name()]["bytes_written"] = io_counters.write_bytes
        check_results[process.name()]["disk_usage"] = disk_usage_process/disk_total * 100


def check_processes(time, binary_list, host_name, csv_log_file):
    """
    Check the CPU, memory and file descriptors for each processes.
    :param time: seconds between each scan.
    :param binary_list: list of binaries to monitor
    :param host_name: name used to identify the machine
    :param csv_log_file: name used for the CSV file
    """
    # More info about this at: https://psutil.readthedocs.io/en/latest/index.html
    base_dict = {"current_cpu": 0.0, "current_virtual_memory_usage": 0.0,
                 "current_resident_set_size": 0.0, "current_memory_usage": 0.0,
                 "current_file_descriptors": 0, "read_ops": 0, "write_ops": 0,
                 "current_unique_set_size_memory": 0.0, "current_proportional_set_size_memory": 0.0,
                 "current_swapping_memory": 0.0, "bytes_read": 0,
                 "bytes_written": 0, "disk_usage": 0}

    StateData = namedtuple('StateData', ['state_file_type', 'path'])

    bin_data = {w_bin: dict(base_dict) for w_bin in binary_list}

    first_iteration = True

    # Capture Ctrl + C
    signal(SIGINT, signal_handler)
    while True:
        # Compute the difference between the last check and the new one
        # and show the info through de stdout
        try:
            if first_iteration: first_iteration = False

            threads = []
            dead_processes = set(binary_list)

            running_processes = [psutil.Process(x.pid) for x in
                                 filter(lambda x: x.name() in binary_list, psutil.process_iter())]

            for process in running_processes:
                if process.is_running():
                    if process.name() in dead_processes:
                        dead_processes.remove(process.name())

                thread = Thread(target=compute_diff, args=(bin_data, process))
                threads.append(thread)
                thread.start()

            for dead_process in dead_processes:
                bin_data[dead_process] = dict(base_dict)

            for trd in threads:
                trd.join()

        except psutil.NoSuchProcess:
            logger.exception("Process not found")
        except KeyError:
            logger.exception("Error getting something from a dict")
        except IOError as io_err:
            logger.exception("Couldn't access the file")
        except Exception:
            logger.exception("Generic error")
        finally:
            write_csv(bin_data, "binaries", csv_log_file)

        sleep(time)


def monitor(time, host_name, binaries):
    csv_log_file = "monitor-{}.csv".format(host_name)
    check_processes(time, binaries, host_name, csv_log_file)


def main():
    parser = argparse.ArgumentParser()
    ####################################################################################################################
    parser.add_argument('-s', '--sleep', type=float, dest='time',
                        help="Sleep time in seconds between each scan")
    parser.add_argument('-b', '--binaries', nargs='+', type=str, dest='binaries',
                        help="Monitor specific binaries. Default: all")
    parser.add_argument('-n', '--name', type=str, dest='host_name',
                        help="Set the name of the host. Used to write the CSV file")
    parser.add_argument('-d', dest='debug_level', action='count', help="Set log level to debug")
    args = parser.parse_args()

    if not args.time or not args.host_name:
        logger.critical("sleep and name paramaters are needed.")
        exit(1)

    if args.debug_level is not None:
        logger.setLevel(logging.DEBUG)

    if not args.binaries:
        logger.critical("Binaries to measure should be explicitly defined when calling the script.")
        exit(1)
    else:
        binaries = args.binaries

    monitor(args.time, args.host_name, binaries)


if __name__ == "__main__":
    main()
