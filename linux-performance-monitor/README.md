# linux-performance-monitor
Continuously monitor the CPU and memory usage of the specified process in the Linux system.
According to the need, you can save the monitoring results to the excel table, or MySQL database

## Usage
1. clone linux-performance-monitor repository
   ```shell
   git clone http
   
   cd Small_Tool/linux-performance-monitor
   ```

2. set the `PID`, `the monitoring time`, linux's `username` and `password`, etc.

3. run
   ```shell
   python linux-performance-monitor.py
   ```
   
## Requirements
1. paramiko
2. pymysql
