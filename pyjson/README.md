# pyjson
Compare two similar json files.
If some fields are missing or the value of a field is different, an error message will be displayed.

## Usage
1. install package using `pip`
    ```shell
    pip install pyjson
    ```
    
2. Save two json files to `.txt` format, then run
   ```shell
   pyjson.compare('1.txt', '2.txt')
   ```
