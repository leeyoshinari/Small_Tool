# timeoutLimit
It's used to avoid function run timeout.
When a function runs for a long time, or running is stuck but no error, you need to determine whether the function runs timeout. If timeout, jumping out of the function and some message should be returned.
With the Python decorator, it's possible to introduce a timing function without affecting the original function.

## Usage
1. clone timeoutLimit repository
   ```shell
   git clone https://github.com/leeyoshinari/Small_Tool.git
   
   cd Small_Tool/timeoutLimit
   ```

2. Example
   ```shell
   import time
   from xxx/timeout import timeoutlimit
   
   @timeoutlimit(3)
   def sleep():
		time.sleep(5)
		return True
	
	print(sleep())
   ```
   ```shell
   The output: None
   ```

3. Others
   If a function runs timeout, it returns None, else, it returns the result of the function.
